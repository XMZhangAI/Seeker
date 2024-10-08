import os
import json
import re
from gpt_call import gpt_call
import prompt
import argparse

# Load cee.json
def load_cee(cee_file):
    with open(cee_file, 'r', encoding='utf-8') as f:
        cee = json.load(f)
    return cee

# Function to read the input code file
def read_code_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()
    return code

# Planner agent
def planner_agent(codebase):
    planner_prompt = prompt.planner_prompt.format(codebase=codebase)
    response = gpt_call("gpt-4o", planner_prompt)
    
    # Extract units from the response
    units = {}
    unit_pattern = r'Unit\s+(\d+):\s*\[Code Segment\]\s*(.*?)\s*(?=Unit\s+\d+:|\Z)'
    matches = re.finditer(unit_pattern, response, re.DOTALL)
    for match in matches:
        unit_number = int(match.group(1))
        unit_code = match.group(2).strip()
        units[unit_number] = unit_code
    return units

# Function to get exception branches from cee.json
def get_exception_branches(cee):
    branches = []
    for child in cee.get('children', []):
        if child['name'] == 'Error' or child['name'] == 'Exception':
            branches.extend(child.get('children', []))
    return branches

# Detector agent
def detector_agent(unit_code, cee):
    # Extract all exception branches
    exception_branches = get_exception_branches(cee)

    # Prepare the scenario descriptions
    scenario_desc = ""
    for branch in exception_branches:
        scenario_desc += f"{branch['name']}: {branch.get('scenario', '')}\n"
        
    # Prepare the property descriptions
    property_desc = ""
    for branch in exception_branches:
        property_desc += f"{branch['name']}: {branch.get('property', '')}\n"

    # Use the detector_scenario_match
    detector_prompt = prompt.detector_scenario_match.format(scenario=scenario_desc, code=unit_code)
    response = gpt_call("gpt-4o", detector_prompt)
    
    # Parse the response to get code_with_label
    try:
        labels = json.loads(response)
        code_with_label = labels.get("code_with_label", {})
    except json.JSONDecodeError:
        code_with_label = {}

    # Get the list of exception branches that are matched in the code
    matched_branches = set()
    for line_number, label in code_with_label.items():
        if label != "None":
            matched_branches.update([l.strip() for l in label.split(',')])

    matched_branches = list(matched_branches)
    
    # Use the detector_prop_match(Union Set)
    detector_prompt = prompt.detector_prop_match.format(property=property_desc, code=unit_code)
    response = gpt_call("gpt-4o", detector_prompt)
    
    # Parse the response to get code_with_label
    try:
        labels = json.loads(response)
        code_with_label = labels.get("code_with_label", {})
    except json.JSONDecodeError:
        code_with_label = {}
        
    # Get the list of exception branches that are matched in the code
    matched_branches_prop = list()
    for line_number, label in code_with_label.items():
        if label != "None":
            matched_branches_prop.extend([l.strip() for l in label.split(',')])
    
    matched_branches = list(set(matched_branches + matched_branches_prop))
    
    return matched_branches

# Predator agent
def predator_agent(unit_code, code_summary, exception_branches_list):
    # Use the predator_prompt
    exception_branches_str = ', '.join(exception_branches_list)
    predator_prompt = prompt.predator_prompt.format(
        code_unit=unit_code,
        code_summary=code_summary,
        exception_branches=exception_branches_str
    )
    response = gpt_call("gpt-4o", predator_prompt)

    # Parse the response to get ExceptionNodes
    try:
        exception_nodes = json.loads(response).get('ExceptionNodes', [])
    except json.JSONDecodeError:
        exception_nodes = []
    return exception_nodes

def code_summary(unit_code):
    summary_prompt = prompt.code_summary_prompt.format(code_unit=unit_code)
    response = gpt_call("gpt-4", summary_prompt)

    # Extract the summary from the response
    try:
        summary_match = re.search(r'\[Code Summary\]\s*(.*)', response, re.DOTALL)
        if summary_match:
            code_summary = summary_match.group(1).strip()
        else:
            code_summary = "No summary provided."
    except Exception as e:
        print(f"Error extracting code summary: {e}")
        code_summary = "No summary provided."

    return code_summary

# Function to get handling strategy from cee.json
def get_handling_strategy(cee, exception_name):
    # Search cee for the exception node with the given name
    def search_exception(node, name):
        if node['name'] == name:
            return node
        for child in node.get('children', []):
            result = search_exception(child, name)
            if result:
                return result
        return None

    exception_node = search_exception(cee, exception_name)
    if exception_node:
        return exception_node.get('info', {}).get('handle_logic', '')
    else:
        return ''
    
# Function to get CEE info for an exception
def get_cee_info(cee, exception_name):
    # Search cee for the exception node with the given name
    def search_exception(node, name):
        if node['name'] == name:
            return node
        for child in node.get('children', []):
            result = search_exception(child, name)
            if result:
                return result
        return None

    exception_node = search_exception(cee, exception_name)
    if exception_node:
        return exception_node.get('info', {})
    else:
        return {}

# Ranker agent updated to use GPT-4
def ranker_agent(cee, exception_nodes):
    # Prepare the input for the prompt
    exceptions_info = []
    for exception in exception_nodes:
        exception_type = exception.get('ExceptionType', '')
        cee_info = get_cee_info(cee, exception_type)
        handling_strategy = cee_info.get('handle_logic', 'No handling strategy available.')
        exception_info = {
            "ExceptionType": exception_type,
            "HandlingStrategy": handling_strategy,
            "CEE_Info": cee_info
        }
        exceptions_info.append(exception_info)
    
    # Prepare the prompt
    ranker_input = {
        "ExceptionNodes": exceptions_info
    }
    ranker_prompt = prompt.ranker_prompt.format(exception_nodes=json.dumps(ranker_input, indent=4))
    
    # Call GPT-4
    response = gpt_call("gpt-4o", ranker_prompt)
    
    # Parse the response
    try:
        rankings = json.loads(response)
    except json.JSONDecodeError:
        print("Error parsing GPT response in Ranker agent.")
        rankings = {"Exceptions": []}
    
    return rankings

# Handler agent
def handler_agent(unit_code, handling_strategies):
    handler_prompt = prompt.handler_prompt.format(
        code_unit=unit_code,
        strategy1=handling_strategies
    )
    response = gpt_call("gpt-4o", handler_prompt)
    # Extract optimized code from the response
    optimized_code_match = re.search(r'\[Optimized Code\]\s*(.*)', response, re.DOTALL)
    if optimized_code_match:
        optimized_code = optimized_code_match.group(1).strip()
    else:
        optimized_code = unit_code  # Fallback to original code if parsing fails
    return optimized_code

# Function to combine optimized units
def combine_units(units):
    combined_code = ''
    for unit_number in sorted(units.keys()):
        combined_code += units[unit_number] + '\n'
    return combined_code

def main(input_file, output_file, cee_file):
    # Load the CEE
    cee = load_cee(cee_file)
    # Read the input codebase
    codebase = read_code_file(input_file)
    # Planner agent: Segment the codebase
    units = planner_agent(codebase)
    
    optimized_units = {}
    for unit_number, unit_code in units.items():
        # Detection phase: Detector agent
        matched_branches = detector_agent(unit_code, cee)
        # Retrieval phase: Predator agent
        code_summary_ = code_summary(unit_code)
        exception_nodes = predator_agent(unit_code, code_summary_, matched_branches)
        # Mapping relevant exception handling strategies from CEE
        handling_strategies = ''
        for exception in exception_nodes:
            exception_type = exception.get('ExceptionType', '')
            strategy = get_handling_strategy(cee, exception_type)
            if strategy:
                handling_strategies += f"Exception: {exception_type}\nHandling Strategy: {strategy}\n\n"
        if not handling_strategies:
            handling_strategies = "No specific handling strategies found."
        # Ranking phase: Ranker agent
        rankings = ranker_agent(exception_nodes)
        # Handling phase: Handler agent
        # Filter exceptions based on grade threshold
        grade_threshold = 0.5
        selected_exceptions = []
        for exception in rankings.get("Exceptions", []):
            if exception.get("LikelihoodScore", 0) > grade_threshold:
                selected_exceptions.append(exception)
        # Prepare handling strategies for selected exceptions
        selected_handling_strategies = ''
        for exception in selected_exceptions:
            exception_type = exception.get('ExceptionType', '')
            strategy = get_handling_strategy(cee, exception_type)
            if strategy:
                selected_handling_strategies += f"Exception: {exception_type}\nHandling Strategy: {strategy}\n\n"
        if not selected_handling_strategies:
            selected_handling_strategies = "No specific handling strategies found."
        optimized_code = handler_agent(unit_code, selected_handling_strategies)  
        # Store the optimized unit
        optimized_units[unit_number] = optimized_code
    
    # Combine optimized units
    optimized_codebase = combine_units(optimized_units)
    
    # Write the optimized code to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(optimized_codebase)
    
    print(f"Optimized code has been written to {output_file}")

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Seeker Pipeline for Exception Handling Enhancement')
    parser.add_argument('--code_path', type=str, required=True, help='Path to the input code file')
    parser.add_argument('--output_path', type=str, required=True, help='Path to write the optimized code')
    parser.add_argument('--cee_path', type=str, default='cee.json', help='Path to the cee.json file')
    args = parser.parse_args()
    input_file = args.code_path
    output_file = args.write_path
    cee_file = args.cee_path
    main(input_file, output_file, cee_file)

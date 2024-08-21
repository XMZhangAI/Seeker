import json
from tqdm import tqdm
from gpt_call import *
from prompt import *

with open ("functions_with_label.jsonl", "r", encoding='utf-8') as f:
    functions = [json.loads(line) for line in f]
    
with open ("throwable_tree_with_scenario.json", "r", encoding='utf-8') as f:
    throwable_tree = json.load(f)

def get_scenario_list(node):
    scenarios = []
    if 'scenario' in node:
        scenarios.append(node['scenario'])
    for child in node['children']:
        scenarios += get_scenario_list(child)
    return scenarios
            
scenarios = get_scenario_list(throwable_tree)

error_functions = []
 
def test(function, scenarios):
    try:
        gpt_answers = []
        gpt_labels = []
        for scenario in scenarios:
            prompt = check.format(code=function['function_body'], scenario=scenario)
            response = gpt_call("gpt-4o", prompt)
            response = eval(response.replace("```", "").replace("json", "").replace("，",",").strip())
            response["scenario"] = scenario
            print(response)
            gpt_answers.append(response)
            if response["answer"] == "1":
                gpt_labels.append(scenario)
        function['gpt_answers'] = gpt_answers
        function['gpt_labels'] = gpt_labels
    except Exception as e:
        print(e)
        error_functions.append(function)
        
for function in tqdm(functions):
    test(function, scenarios)
    
with open("functions_with_gpt_label.jsonl", "w", encoding='utf-8') as f:
    for function in functions:
        f.write(json.dumps(function, ensure_ascii=False) + '\n')
        
with open("error_functions.json", "w", encoding='utf-8') as f:
    f.write(json.dumps(error_functions, ensure_ascii=False) + '\n')

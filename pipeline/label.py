import json

with open ("functions_with_cleaned_body.jsonl", "r", encoding='utf-8') as f:
    functions = [json.loads(line) for line in f]
    
with open ("throwable_tree_with_scenario.json", "r", encoding='utf-8') as f:
    throwable_tree = json.load(f)

def pass_scenario(node):
    if 'scenario' in node:
        for child in node['children']:
            if 'scenario' not in child:
                child['scenario'] = node['scenario']
    for child in node['children']:
        pass_scenario(child)
            
pass_scenario(throwable_tree)
 
def get_scenario(catch, node):
    scenario = None
    if catch == node['name'] and 'scenario' in node:
        scenario = node['scenario']
    else:
        for child in node['children']:
            scenario = get_scenario(catch, child)
            if scenario:
                break
    return scenario
    
def label(function, throwable_tree):
    catch_types = function["catch_types"]
    scenarios = []
    for catch in catch_types:
        scenario = get_scenario(catch, throwable_tree)
        if scenario:
            scenarios.append(scenario)
    function['scenarios'] = scenarios
    
for function in functions:
    label(function, throwable_tree)
    
with open("functions_with_label.jsonl", "w", encoding='utf-8') as f:
    for function in functions:
        f.write(json.dumps(function, ensure_ascii=False) + '\n')

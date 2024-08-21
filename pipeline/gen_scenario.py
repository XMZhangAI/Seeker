from prompt import *
from gpt_call import *
import json
from tqdm import tqdm

with open ("throwable_tree_with_info.json", "r", encoding='utf-8') as f:
    throwable_tree = json.load(f)

with open ("sample_scenario.json", "r", encoding='utf-8') as f:
    sample_scenario = json.load(f)

error_nodes = []
  
def get_scenario(node):
    try:
        ename = node["name"]
        info = node["info"]
        prompt = genscenario.format(sample_desc=sample_scenario, ename=ename)
        response = gpt_call("gpt-4o", prompt)
        response = eval(response.replace("```", "").replace("json", "").replace("，",",").strip())
        node["scenario"] = response["scenario"]
        print(response)
    except Exception as e:
        error_nodes.append(node)
        print(e)
    # for child in node["children"]:
    #     get_info(child)
        
# get_info(throwable_tree)
error_tree = throwable_tree["children"][0]
exception_tree = throwable_tree["children"][1]

for direct_subclass in tqdm(error_tree["children"]):
    get_scenario(direct_subclass)
    
for direct_subclass in tqdm(exception_tree["children"]):
    get_scenario(direct_subclass)

with open("throwable_tree_with_scenario.json", "w", encoding='utf-8') as f:
    json.dump(throwable_tree, f, ensure_ascii=False, indent=4)

with open("error_nodes.json", "w", encoding='utf-8') as f:
    json.dump(error_nodes, f, ensure_ascii=False, indent=4)
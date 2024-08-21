from prompt import *
from gpt_call import *
import json

with open ("throwable_tree_with_info______.json", "r", encoding='utf-8') as f:
    throwable_tree = json.load(f)

error_nodes = []
  
def get_info(node):
    ename = node["name"]
    prompt = geninfo.format(ename=ename)
    try:
        if "info" not in node:
            response = gpt_call("gpt-4", prompt)
            response = eval(response.replace("```", "").replace("json", "").replace("，",",").strip())
            node["info"] = response
            print(response)
    except Exception as e:
        error_nodes.append(node)
        print(e)
    for child in node["children"]:
        get_info(child)
        
get_info(throwable_tree)

with open("throwable_tree_with_info_______.json", "w", encoding='utf-8') as f:
    json.dump(throwable_tree, f, ensure_ascii=False, indent=4)

with open("error_nodes.json", "w", encoding='utf-8') as f:
    json.dump(error_nodes, f, ensure_ascii=False, indent=4)
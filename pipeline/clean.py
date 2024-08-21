from gpt_call import *
from prompt import *
import json
from tqdm import tqdm

with open ("functions_with_catch.jsonl", "r", encoding='utf-8') as f:
    functions_with_catch = [json.loads(line) for line in f]
    
error_nodes = []

for function in tqdm(functions_with_catch):
    try:
        function_body = function['function_body']
        prompt = remove.format(code=function_body)
        response = gpt_call("gpt-4o", prompt)
        response = eval(response.replace("```", "").replace("json", "").replace("，",",").strip())
        function["cleaned_code"] = response["cleaned_code"]
        # function["complete_code"] = response["complete_code"]
        print(response)
    except Exception as e:
        error_nodes.append(function)
        print(e)
        
with open("functions_with_cleaned_body.jsonl", "w", encoding='utf-8') as f:
    for function in functions_with_catch:
        f.write(json.dumps(function, ensure_ascii=False) + '\n')
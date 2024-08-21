import json

with open ("functions_with_gpt_label.jsonl", "r", encoding='utf-8') as f:
    functions = [json.loads(line) for line in f]
    
for function in functions:
    try:
        print(function['function_name'])
        print("GPT labels: ", function['gpt_labels'])
        print("Scenarios: ", function['scenarios'])
    except:
        pass
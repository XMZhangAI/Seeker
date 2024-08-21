import os
import javalang
import json
import re
from gpt_call import *
from prompt import *

def get_code_from_line_range(code, start_line, end_line):
    lines = code.split('\n')
    return '\n'.join(lines[start_line - 1:end_line])

def extract_try_catch_functions_from_java_files(directory):
    functions_with_catch = []

    # 遍历目录中的所有文件
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".java"):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as java_file:
                    code = java_file.read()
                    try:
                        # 解析Java代码
                        tree = javalang.parse.parse(code)
                        # 遍历所有类定义
                        for path, node in tree.filter(javalang.tree.MethodDeclaration):
                            # 检查是否包含try-catch块
                            try_catch_blocks = list(node.filter(javalang.tree.TryStatement))
                            if try_catch_blocks:
                                catch_types = []
                                for _, try_block in try_catch_blocks:
                                    if not try_block.catches:
                                        continue
                                    for catch_clause in try_block.catches:
                                        # 收集所有catch的异常类型
                                        catch_types.extend(catch_clause.parameter.types)
                                # 构建一个包含函数体和异常类型的JSON对象
                                func_start = node.position.line
                                func_end = node.body[-1].position.line
                                function_body = get_code_from_line_range(code, func_start, func_end)
                                function_info = {
                                    'file_path': file,
                                    'function_name': node.name,
                                    'function_line_range': [func_start, func_end],
                                    'function_body': function_body,
                                    'catch_types': catch_types
                                }
                                functions_with_catch.append(function_info)
                    except javalang.parser.JavaSyntaxError:
                        print(f"Syntax error in file: {path}")
    
    return functions_with_catch

# 调用函数，需要指定Java代码所在的文件夹路径
java_folder_path = 'java_codes'  # 假设你的Java文件夹名为 'java_codes'
results = extract_try_catch_functions_from_java_files(java_folder_path)
with open('functions_with_catch.jsonl', 'w', encoding='utf-8') as f:
    for result in results:
        f.write(json.dumps(result, ensure_ascii=False) + '\n')
import os
import re
import tempfile
import ast
import difflib
import Levenshtein
import openai
from pylint import epylint as lint
import argparse

# 1. Automated Code Review Score (ACRS)
def calculate_acrs(original_code, processed_code, standard_code):
    """
    Calculates the Automated Code Review Score (ACRS) for the processed code.
    """
    acrs = evaluate_code_with_gpt4(processed_code)
    return acrs

# Function to get sensitive code lines (lines within try-except blocks)
def get_sensitive_code_lines(code):
    tree = ast.parse(code)
    sensitive_lines = set()

    class TryExceptVisitor(ast.NodeVisitor):
        def __init__(self):
            self.current_try_lines = set()
            super().__init__()

        def visit_Try(self, node):
            for n in ast.walk(node):
                if hasattr(n, 'lineno'):
                    self.current_try_lines.add(n.lineno)
            self.generic_visit(node)

    visitor = TryExceptVisitor()
    visitor.visit(tree)
    sensitive_lines = visitor.current_try_lines
    return sensitive_lines

# 2. Coverage (COV)
def calculate_cov(original_code, processed_code, standard_code):
    """
    Calculates the Coverage (COV) metric.
    """
    actual_sensitive_lines = get_sensitive_code_lines(standard_code)
    detected_sensitive_lines = get_sensitive_code_lines(processed_code)
    correct_detected_sensitive_lines = actual_sensitive_lines & detected_sensitive_lines

    if len(actual_sensitive_lines) == 0:
        cov = 1.0
    else:
        cov = len(correct_detected_sensitive_lines) / len(actual_sensitive_lines)

    return cov

# Function to get try-blocks in the code
def get_try_blocks(code):
    tree = ast.parse(code)
    try_blocks = []

    class TryBlockVisitor(ast.NodeVisitor):
        def visit_Try(self, node):
            start_line = node.lineno
            end_line = max([n.lineno for n in ast.walk(node) if hasattr(n, 'lineno')])
            try_blocks.append((start_line, end_line))
            self.generic_visit(node)

    visitor = TryBlockVisitor()
    visitor.visit(tree)
    return try_blocks

# 3. Coverage Pass (COV-P)
def calculate_cov_p(original_code, processed_code, standard_code):
    """
    Calculates the Coverage Pass (COV-P) metric.
    """
    actual_try_blocks = get_try_blocks(standard_code)
    detected_try_blocks = get_try_blocks(processed_code)

    correct_try_blocks = [block for block in detected_try_blocks if block in actual_try_blocks]
    incorrectly_detected_try_blocks = [block for block in detected_try_blocks if block not in actual_try_blocks]

    denominator = len(actual_try_blocks) + len(incorrectly_detected_try_blocks)

    if denominator == 0:
        cov_p = 1.0
    else:
        cov_p = len(correct_try_blocks) / denominator

    return cov_p

# Function to get exception types from the code
def get_exception_types(code):
    tree = ast.parse(code)
    exception_types = []

    class ExceptionTypeVisitor(ast.NodeVisitor):
        def visit_ExceptHandler(self, node):
            if node.type is not None:
                if isinstance(node.type, ast.Name):
                    exception_types.append(node.type.id)
                elif isinstance(node.type, ast.Tuple):
                    for e in node.type.elts:
                        if isinstance(e, ast.Name):
                            exception_types.append(e.id)
            self.generic_visit(node)

    visitor = ExceptionTypeVisitor()
    visitor.visit(tree)
    return exception_types

# 4. Accuracy (ACC)
def calculate_acc(original_code, processed_code, standard_code):
    """
    Calculates the Accuracy (ACC) of the exception types identified.
    """
    actual_exception_types = get_exception_types(standard_code)
    detected_exception_types = get_exception_types(processed_code)
    total_exception_types_identified = len(detected_exception_types)

    correct_exception_types = 0
    for exc in detected_exception_types:
        if exc in actual_exception_types:
            correct_exception_types += 1
        else:
            exc_class = getattr(__builtins__, exc, None)
            for actual_exc in actual_exception_types:
                actual_exc_class = getattr(__builtins__, actual_exc, None)
                if actual_exc_class and exc_class and issubclass(exc_class, actual_exc_class):
                    correct_exception_types += 1
                    break

    if total_exception_types_identified == 0:
        acc = 1.0
    else:
        acc = correct_exception_types / total_exception_types_identified

    return acc

# Function to get the code of try-catch blocks
def get_try_catch_blocks_code(code):
    tree = ast.parse(code)
    try_catch_blocks = []

    class TryCatchCodeVisitor(ast.NodeVisitor):
        def __init__(self, code_lines):
            self.code_lines = code_lines

        def visit_Try(self, node):
            start_line = node.lineno - 1
            end_line = max([n.lineno for n in ast.walk(node) if hasattr(n, 'lineno')]) - 1
            block_code = '\n'.join(self.code_lines[start_line:end_line + 1])
            try_catch_blocks.append(block_code)
            self.generic_visit(node)

    code_lines = code.split('\n')
    visitor = TryCatchCodeVisitor(code_lines)
    visitor.visit(tree)
    return try_catch_blocks

# 5. Edit Similarity (ES)
def calculate_es(original_code, processed_code, standard_code):
    """
    Calculates the Edit Similarity (ES) between the generated and actual try-catch blocks.
    """
    generated_try_catch_blocks = get_try_catch_blocks_code(processed_code)
    actual_try_catch_blocks = get_try_catch_blocks_code(standard_code)

    generated_code = '\n'.join(generated_try_catch_blocks)
    actual_code = '\n'.join(actual_try_catch_blocks)

    distance = Levenshtein.distance(generated_code, actual_code)
    max_len = max(len(generated_code), len(actual_code))
    if max_len == 0:
        similarity = 1.0
    else:
        similarity = 1 - distance / max_len

    return similarity

# Function to evaluate code using GPT-4 (requires OpenAI API key)
def evaluate_code_with_gpt4(code_snippet):
    # openai.api_key = 'YOUR_API_KEY'

    prompt = f"Please review the following code for exception handling practices and evaluate whether it's good or bad according to engineering best practices. Provide a single word answer: 'good' or 'bad'.\n\nCode:\n{code_snippet}"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt},
        ],
        max_tokens=1,
        n=1,
        stop=None,
        temperature=0,
    )

    answer = response['choices'][0]['message']['content'].strip().lower()
    if 'good' in answer:
        return 'good'
    else:
        return 'bad'

# 6. Code Review Score (CRS)
def calculate_crs(original_code, processed_code, standard_code):
    """
    Calculates the Code Review Score (CRS) based on GPT-4 evaluation.
    """
    generated_try_catch_blocks = get_try_catch_blocks_code(processed_code)
    total_evaluations = len(generated_try_catch_blocks)
    good_evaluations = 0

    for block in generated_try_catch_blocks:
        evaluation = evaluate_code_with_gpt4(block)
        if evaluation == 'good':
            good_evaluations += 1

    if total_evaluations == 0:
        crs = 1.0
    else:
        crs = good_evaluations / total_evaluations

    return crs

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Calculate code evaluation metrics.')
    parser.add_argument('original_code_path', type=str, help='Path to the original code file.')
    parser.add_argument('processed_code_path', type=str, help='Path to the processed code file.')
    parser.add_argument('standard_code_path', type=str, help='Path to the standard code file.')
    args = parser.parse_args()
    
    with open(args.original_code_path, 'r') as file:
        original_code = file.read()
    with open(args.processed_code_path, 'r') as file:
        processed_code = file.read()
    with open(args.standard_code_path, 'r') as file:
        standard_code = file.read()

    acrs = calculate_acrs(original_code, processed_code, standard_code)
    print(f"Automated Code Review Score (ACRS): {acrs}")

    cov = calculate_cov(original_code, processed_code, standard_code)
    print(f"Coverage (COV): {cov}")

    cov_p = calculate_cov_p(original_code, processed_code, standard_code)
    print(f"Coverage Pass (COV-P): {cov_p}")

    acc = calculate_acc(original_code, processed_code, standard_code)
    print(f"Accuracy (ACC): {acc}")

    es = calculate_es(original_code, processed_code, standard_code)
    print(f"Edit Similarity (ES): {es}")

    crs = calculate_crs(original_code, processed_code, standard_code)
    print(f"Code Review Score (CRS): {crs}")

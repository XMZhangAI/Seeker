geninfo = \
"""Below is a kind of error/exception in java. Please first discribe the error/exception definition, then explain the typical reasons and dangerous operations to raise the error/exception and finally provide a sample code that will raise the error/exception, and the a code snippet that will handle the error/exception.(for example, by using try-catch block)

[Error/Exception]
{ename}

Note you should output in the json format like below:
{{
    "definition": ...,
    "reasons": ...,
    "dangerous_operations": ...,
    "sample_code": ...,
    "handle_code": ...
}}
"""

genscenario = \
"""Below is a kind of exception in java. Please according to the sample discription of scenario of errortype, provide a scenario description of the exception in java just like the sample description.Please note that the granularity of the scenario descriptions you generate should be consistent with the examples.

[Sample Description]
{sample_desc}

[Exception]
{ename}

Note you should output in the json format like below, please note that the granularity of the scenario descriptions you generate should be consistent with the examples.:
{{
    "scenario": ...
}}
"""

genproperty = \
"""Below is a kind of exception in java and its scenario description. Please according to the sample discription of scenario and property of errortype, provide a property description of the exception in java just like the sample description. You can alse adjust the given scenario description to make them consistent. Please note that the granularity of the property descriptions you generate should be consistent with the examples.

[Sample Description]
{sample_desc}

[Exception]
{ename}

[Scenario Description]
{scenario}

Note you should output in the json format like below, please note that the granularity of the property descriptions you generate should be consistent with the examples.:
{{
    "scenario": ...;
    "property": ...
}}
"""

planner_prompt = \
"""You are a software engineer tasked with analyzing a codebase. Your task is to segment the given codebase into manageable units for further analysis. The criteria for segmentation are:

- Each unit should have a length within 200 lines.
- The function nesting level should be low.
- The logical flow should be clear and self-contained.
- The segment should be complete and readable.

Given the following codebase:

[Codebase]
{codebase}

Please segment the codebase into units and list them as:

Unit 1:
[Code Segment]
{unit1}

Unit 2:
[Code Segment]
{unit2}

...

Ensure that each unit complies with the criteria specified above.
"""

detector_senario_match = \
"""You are a java code auditor. You will be given a doc describe different exception scenarios and a java code snippet.

Your task is to label each line of the code snippet with the exception scenario that it belongs to. If a line does not belong to any scenario, label it with "None". If a line belongs to one of the given scenarios, label it with all the scenarios it belongs to.

[Scenario description]
{scenario}

[Java code]
{code}

Please output the labeling result in the json format like below:
{{
    "code_with_label": ...
}}
"""

detector_prop_match = \
"""You are a java code auditor. You will be given a doc describe different exception properties and a java code snippet.

Your task is to label each line of the code snippet with the exception property that it belongs to. If a line does not belong to any property, label it with "None". If a line belongs to one of the given properties, label it with all the properties it belongs to.

[property description]
{property}

[Java code]
{code}

Please output the labeling result in the json format like below:
{{
    "code_with_label": ...
}}
"""

predator_prompt = \
"""You are a code analysis assistant. Your task is to process the given code unit and identify specific exception types that may be thrown.

[Code Unit]
{code_unit}

[Code Summary]
{code_summary}

Based on the code summary and the potential exception branches provided, identify the specific exception nodes that may be thrown.

[Potential Exception Branches]
{exception_branches}

Please answer in the following JSON format:

{
    "ExceptionNodes": [
        {
            "ExceptionType": "ExceptionType1",
        },
        {
            "ExceptionType": "ExceptionType2",
        },
        ...
    ]
}

Ensure that your response strictly follows the specified format.
"""

code_summary_prompt = """
You are a software engineer tasked with summarizing a code unit. Please provide a concise summary of the code's functionality at the function level.

[Code Unit]
{code_unit}

Please provide the summary in the following format:

[Code Summary]
{{code_summary}}

Ensure that your summary is clear and captures the main functionality of the code unit.
"""

ranker_prompt = \
"""You are an exception ranking assistant. Your task is to assign grades to the identified exceptions based on their likelihood and the suitability of their handling strategies.

For each exception, please calculate:

- Exception Likelihood Score (from 0 to 1) based on its attributes and impact.
- Suitability Score (from 0 to 1) of the proposed handling strategy.

[Identified Exceptions and Handling Strategies]
{
    "ExceptionNodes": [
        {
            "ExceptionType": "ExceptionType1",
            "HandlingStrategy": "{strategy1}",
            "CEE_Info": "{info1}"
        },
        ...
    ]
}

Provide your calculations and the final grades in the following JSON format:

{
    "Exceptions": [
        {
            "ExceptionType": "ExceptionType1",
            "LikelihoodScore": value,
            "SuitabilityScore": value,
        },
        ...
    ]
}

Please ensure your response adheres to the specified format.

"""

handler_prompt = \
"""You are a software engineer specializing in exception handling. Your task is to optimize the given code unit by applying appropriate exception handling strategies.

[Code Unit]
{code_unit}

[Handling Strategy]
{strategy1}

Generate the optimized code with the applied exception handling strategies.

Please provide the optimized code in the following format:

[Optimized Code]
{optimized_code}

Ensure that the code is syntactically correct and adheres to best practices in exception handling.

"""
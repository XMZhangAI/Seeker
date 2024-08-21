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
"""Below is a kind of error/exception in java. Please according to the sample discription of scenario of errortype in the smart contract, provide a scenario description of the error/exception in java just like the sample description.Please note that the granularity of the scenario descriptions you generate should be consistent with the examples.

[Sample Description]
{sample_desc}

[Error/Exception]
{ename}

Note you should output in the json format like below, please note that the granularity of the scenario descriptions you generate should be consistent with the examples.:
{{
    "scenario": ...
}}
"""

remove = \
"""Below is a java fuction code with exception handling. Please remove the exception handling code, for example, by removing the code in the catch block and the try-catch statement(but keep the try code).
{code}
You should output the code after removing the exception handling code in the json format like below:
{{
    "cleaned_code": ...
}}
"""

complete = \
"""Below is a java fuction code with exception handling(might not be complete). Please check if the function is complete, if not, finish it in the end in any reasonable ways.
{code}
You should output the complete function code in the json format like below:
{{
    "complete_code": ...
}}
"""

check = \
"""You are a java code auditor.You will be asked questions related to code scenarios. You can mimic an swering them in the background five times and provide me with the most frequently appearing answer. Furthermore, please strictly adhere to the output format specified in the question;
Your task is scenario matching
Given the following java code, is this code in compliance with the scenario description below? Answer with "0/1" where 0 means no and 1 means yes.
Note that you should be strict with the scenario description. If the code is not much in compliance with the scenario description, the answer should be 0.
[Java code]
{code}
[Scenario description]
{scenario}
Please answer the question in the json format like below:
{{
    "answer": "0/1",
}}
"""

check_line = \
"""You are a java code auditor. You will be given a doc describe different error/exception scenarios and a java code snippet.
Your task is to label each line of the code snippet with the error/exception scenario that it belongs to. If a line does not belong to any scenario, label it with "None".
[Scenario description]
{scenario}
[Java code]
{code}
Please output the labeling result in the json format like below:
{{
    "label": ...
}}
"""
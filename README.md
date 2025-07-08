# Seeker
*Seeker* is a multi-agent framework inspired by expert developer strategies for exception handling. Details of Seeker can be found in our paper "Seeker: Enhancing Exception Handling in Code with a LLM-based Multi-Agent Approach" [Paper]().

## News
We launched the CEE website: https://common-exception-enumeration.github.io/CEE/

## Outline
- [Seeker](#seeker)
  - [News](#news)
  - [Outline](#outline)
  - [Introduction](#introduction)
  - [Released Versions](#released-versions)
  - [Usage](#usage)
  - [CEE](#cee)
    - [Grid-Fine-Tuning](#grid-fine-tuning)
    - [Components](#components)
  - [Metadata](#metadata)
  - [Repositories](#repositories)
  - [Evaluation](#evaluation)
  - [Experiment](#experiment)
    - [Comparison](#comparison)
    - [Leaderboard](#leaderboard)
  - [Citation](#citation)


## Introduction
In real-world software development, improper or missing exception handling can severely impact the robustness and reliability of code. Exception handling mechanisms require developers to detect, capture, and manage exceptions according to high standards, but many developers struggle with these tasks, leading to fragile code. This problem is particularly evident in open-source projects and impacts the overall quality of the software ecosystem.
To address this challenge, we propose *Seeker*, a multi-agent framework inspired by expert developer strategies for exception handling. Seeker uses agents—Scanner, Detector, Predator, Ranker, and Handler—to assist LLMs in detecting, capturing, and resolving exceptions more effectively.
![fig1](https://i.imgur.com/ydFyBVS.png)


  ## Released Versions
  + CEE-Java-1002
    Until October 2024, we introduce CEE-Java-1002, which serves as a foundational resource for enhancing the reliability of exception handling in code generation by Java developers.
    
    ```json
    sample_cee_node = {
      "name": "IOException",
      "children": ["..."],
      "info": {
          "definition": "IOException is a checked exception that is thrown when an input-output operation failed or interrupted. It's a general class of exceptions produced by failed or interrupted I/O operations.",
          "reasons": "There are several reasons that could cause an IOException to be thrown. These include: File not found error, when the file required for the operation does not exist; Accessing a locked file, which another thread or process is currently using; The file system is read only and write operation is performed; Network connection closed prematurely; Lack of access rights.",
          "dangerous_operations": "Operations that could typically raise an IOException include: Reading from or writing to a file; Opening a non-existent file; Attempting to open a socket to a non-existent server; Trying to read from a connection after it's been closed; Trying to change the position of a file pointer beyond the size of the file.",
          "sample_code": "String fileName = 'nonexistentfile.txt'; \n FileReader fileReader = new FileReader(fileName);",
          "handle_code": "String fileName = 'nonexistentfile.txt'; \n try { \n FileReader fileReader = new FileReader(fileName); \n }catch(IOException ex) { \n    System.out.println('An error occurredwhile processing the file ' + fileName); \n    ex.printStackTrace();\n }",
          "handle_logic":"Try the codes attempting to establish connection with a file/stream/network, catch corresponding ioexception and report it, output openpath is suggested."
      },
      "scenario": "attempt to read from or write to a file/stream/network connection",
      "property": "There might be an unexpected issue with accessing the file/stream/network due to reasons like the file not being found, the stream being closed, or the network connection being interrupted"
    }
    ```

  + CEE-Python-1002-Test
    This is conducted by the same pipline with Java version, forming a naive version for Python. It has been used for testing SWE-bench. Now, it is still under review.
  
  ## Usage
  1. Environment Setup
  ```bash
  conda create -n seeker
  conda activate seeker
  pip install -r requirements.txt
  ```
  2. Run the Seeker on your code
  ```bash
  cd pipeline
  python seeker.py --code_path /path/to/your/code --output_path /path/to/output
  ```
  3. Evaluate the generated code
  ```bash
  cd pipeline
  python evaluate.py --original_code_path /path/to/original_code --processed_code_path /path/to/processed_code
  --standard_code_path /path/to/standard_code
  ```

  ## CEE
  Without a comprehensive and standardized document like CEE, developers may struggle to accurately detect and handle exceptions, leading to either overly generic or improperly specific exception management. CEE addresses these challenges by providing a structured and exhaustive repository of exception information, encompassing scenarios, properties, and recommended handling strategies for each exception type. The construction of CEE is guided by three essential rules, each aimed at addressing the complexities of exception management within Java development.
  
  ### Grid-Fine-Tuning
  ![截屏2024-10-08 23.24.31](https://i.imgur.com/lnVbIcI.png)
  
  ### Components
  *Scenario:* This component describes the specific coding situations or environments in which an exception is likely to occur. By analyzing real-world applications and common coding patterns, we can create realistic scenarios that help developers understand when to anticipate particular exceptions. This contextual understanding is critical for effective exception handling, as it allows developers to write more accurate and responsive code.
  
  *Property:* This aspect outlines the characteristics and attributes of each exception. Understanding the properties of an exception, such as its severity, possible causes, and the context of its occurrence, they are vital for appropriate handling. This detailed information allows developers to make informed decisions on how to respond to exceptions based on their inherent properties.
  
  *Handling Logic:* For each exception node, we define best practices for handling the exception. This includes recommended coding strategies, such as specific try-catch blocks, logging mechanisms, and fallback strategies. By incorporating proven handling logic derived from both successful enterprise practices and open-source contributions, we provide a comprehensive guide that assists developers in implementing effective exception management.

  ## Metadata
  To ensure the quality and representativeness of the dataset, we carefully selected projects on GitHub that are both active and large in scale. We applied stringent selection criteria, including the number of stars, forks, and exception handling repair suggestions in the project to ensure that the dataset comprehensively covers the exception handling practices of modern open-source projects. By automating the collection of project metadata and commit history through the GitHub API, and manually filtering commit records related to exception handling, we have constructed a high-quality, representative dataset for exception handling that provides a solid foundation for evaluating Seeker.

  ## Repositories
  ![截屏2024-10-08 23.25.40](https://i.imgur.com/HWyFNZy.png)


  ## Evaluation
  To comprehensively assess the effectiveness of our method, we employ six metrics:

  **1. Automated Code Review Score (ACRS)**

  Based on an automated code review model, this metric evaluates the overall quality of the generated code in terms of adherence to coding standards and best practices.

  $$
    \text{ACRS} = \text{CodeReviewModel}(\text{GeneratedCode})
  $$

  **Explanation**: A higher ACRS indicates better code quality, reflecting well-structured and maintainable code.

  **2. Coverage (COV)**

  This metric measures the coverage of sensitive code detected by the \textbf{Detector} agent compared to the actual sensitive code.

  $$
    \text{COV} = \frac{|\text{Correct Detected Sensitive Code}|}{|\text{Actual Sensitive Code}|}
  $$

  **Explanation**: It quantifies the proportion of actual sensitive code that our method successfully detects. Over-detection (marking more code than necessary) is not penalized.

  **3. Coverage Pass (COV-P)**

  This metric assesses the coverage relation between the try-blocks detected by the \textbf{Predator} agent and the actual code that requires try-catch blocks.

  $$
    \text{COV-P} = \frac{|\text{Correct Try-Blocks}|}{|\text{Actual Try-Blocks}|}
  $$

  **Explanation**: A try-block is considered correct if it exactly matches the actual code lines. Over-marking or under-marking is counted as incorrect. Over-detection is penalized in this metric by including the incorrectly detected try-catch blocks in the denominator while counting them as incorrect (zero) in the numerator, thus reducing the overall Coverage Pass score.

  **4. Accuracy (ACC)**

  This metric evaluates the correctness of the exception types identified by the **Predator** agent compared to the actual exception types.

  $$
    \text{ACC} = \frac{|\text{Correct Exception Types}|}{|\text{Total Exception Types Identified}|}
  $$

  **Explanation**: An exception type is considered correct if it matches the actual exception or is a reasonable subclass of the actual exception type.

  **5. Edit Similarity (ES)**

  This metric computes the text similarity between the generated try-catch blocks after processing by the **Handler agent** and the actual try-catch blocks.

  $$
    \text{ES} = \text{Similarity}(\text{Generated Try-Catch}, \text{Actual Try-Catch})
  $$

  **Explanation**: We use the Levenshtein distance to measure similarity. A higher ES indicates that the generated code closely matches the actual code.

  **6. Code Review Score (CRS)**

  This metric involves submitting the generated try-catch blocks to GPT-4o for evaluation. The language model provides a binary assessment: good or bad.

  $$
    \text{CRS} = \frac{|\text{Good Evaluations}|}{|\text{Total Evaluations}|}
  $$

  **Explanation**: CRS reflects the proportion of generated exception handling implementations that are considered good according to engineering best practices.


  ## Experiment

  ### Comparison
  We conducted experiments using GPT-4o as the agent's internal large model. Our dataset consists of 750 fragile Java code snippets extracted from real-world projects. We compare our method against KPC, traditional RAG, and General Prompting methods. The performance comparison is presented in the following table.
 ![截屏2024-10-08 23.25.41](https://github.com/user-attachments/assets/3c88f59a-5179-4e3e-b5fe-9a22217e88dc)


  ### Leaderboard
  We use different open-source (e.g. Code Llama-34B , WizardCoder-34B, Vicuna-13B) and closed-source(e.g. Claude-2,GPT-3-davinci, GPT-3.5-turbo, GPT-4-turbo, GPT-4o) LLMs as the agent’s internal model to further analyze models’ ability for exception handling. The results are summarized in the following table.
   ![截屏2024-10-08 23.25.41](https://github.com/user-attachments/assets/a672121d-5520-4c22-a317-895503abc063)


  ## Citation
  ```bash
  @article{zhang2024seeker,  
  title={Seeker: Towards Exception Safety Code Generation with Intermediate Language Agents Framework},
  author={Zhang, Xuanming and Chen, Yuxuan and Zheng, Yiming and Zhang, Zhexin and Yuan, Yuan and Huang, Minlie},
  journal={arXiv preprint arXiv:2412.11713},
  year={2024}
}
```


  

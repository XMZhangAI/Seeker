# Seeker
*Seeker* is a multi-agent framework inspired by expert developer strategies for exception handling. Details of Seeker can be found in our paper "Seeker: Enhancing Exception Handling in Code with a LLM-based Multi-Agent Approach" [Paper]().

## News
[10.1] Announced in ICLR 2025, under review.

## Outline
- [Seeker](#seeker)
  - [News](#news)
  - [Outline](#outline)
  - [Introduction](#introduction)
  - [Released Versions](#released-versions)
  - [CEE](#cee)
    - [Grid-Fine-tuning](#grid-fine-tuning)
    - [Components](#components)
  - [Metadata](#metadata)
  - [Repositories](#repositories)
  - [Evaluation](#evaluation)
    - [Detection](#detection)
      - [Coverage Pass](#coverage-pass)
      - [Recall@k](#recallk)
    - [Handling](#handling)
      - [LLMReview](#llmreview)
      - [Pass@k(待定)](#passk待定)
  - [Sensitive Code Detection](#sensitive-code-detection)
    - [Experimental Settings](#experimental-settings)
    - [Leaderboard](#leaderboard)
    - [Detection Baslines](#detection-baslines)
  - [Exception Safety Code Generation](#exception-safety-code-generation)
    - [Experimental Settings](#experimental-settings-1)
    - [Leaderboard](#leaderboard-1)
    - [Handling Baselines](#handling-baselines)
    - [Issue Solving](#issue-solving)
  - [Citation](#citation)


## Introduction
In real-world software development, improper or missing exception handling can severely impact the robustness and reliability of code. Exception handling mechanisms require developers to detect, capture, and manage exceptions according to high standards, but many developers struggle with these tasks, leading to fragile code. This problem is particularly evident in open-source projects and impacts the overall quality of the software ecosystem.
To address this challenge, we propose *Seeker*, a multi-agent framework inspired by expert developer strategies for exception handling. Seeker uses agents—Scanner, Detector, Predator, Ranker, and Handler—to assist LLMs in detecting, capturing, and resolving exceptions more effectively.
<img width="1246" alt="截屏2024-10-08 15 39 02" src="https://github.com/user-attachments/assets/bd416070-e323-4076-b367-af55a078ef1f">


  ## Released Versions
  + CEE-Java-1002
    Until October 2024, we introduce CEE-Java-1002, which serves as a foundational resource for enhancing the reliability of exception handling in code generation by Java developers.
    
    @Cyx：在这里下面放一个Sample

  + CEE-Python-1002-Test
    This is conducted by the same pipline with Java version, forming a naive version for Python. It has been used for testing SWE-bench. Now, it is still under review.
  

  ## CEE
  Without a comprehensive and standardized document like CEE, developers may struggle to accurately detect and handle exceptions, leading to either overly generic or improperly specific exception management. CEE addresses these challenges by providing a structured and exhaustive repository of exception information, encompassing scenarios, properties, and recommended handling strategies for each exception type. The construction of CEE is guided by three essential rules, each aimed at addressing the complexities of exception management within Java development.
  
  ### Grid-Fine-Tuning
  <img width="596" alt="截屏2024-10-08 15 29 48" src="https://github.com/user-attachments/assets/96e2b2fe-7e8f-4419-b788-c7e1db674a28">
  
  ### Components
  *Scenario:* This component describes the specific coding situations or environments in which an exception is likely to occur. By analyzing real-world applications and common coding patterns, we can create realistic scenarios that help developers understand when to anticipate particular exceptions. This contextual understanding is critical for effective exception handling, as it allows developers to write more accurate and responsive code.
  
  *Property:* This aspect outlines the characteristics and attributes of each exception. Understanding the properties of an exception, such as its severity, possible causes, and the context of its occurrence, they are vital for appropriate handling. This detailed information allows developers to make informed decisions on how to respond to exceptions based on their inherent properties.
  
  *Handling Logic:* For each exception node, we define best practices for handling the exception. This includes recommended coding strategies, such as specific try-catch blocks, logging mechanisms, and fallback strategies. By incorporating proven handling logic derived from both successful enterprise practices and open-source contributions, we provide a comprehensive guide that assists developers in implementing effective exception management.

  ## Metadata
  To ensure the quality and representativeness of the dataset, we carefully selected projects on GitHub that are both active and large in scale. We applied stringent selection criteria, including the number of stars, forks, and exception handling repair suggestions in the project to ensure that the dataset comprehensively covers the exception handling practices of modern open-source projects. By automating the collection of project metadata and commit history through the GitHub API, and manually filtering commit records related to exception handling, we have constructed a high-quality, representative dataset for exception handling that provides a solid foundation for evaluating Seeker.

  ## Repositories
<img width="539" alt="截屏2024-10-08 15 34 37" src="https://github.com/user-attachments/assets/30ed584d-31c0-4b5c-a9b4-af538d424f42">

  ## Evaluation
  `指标信息（Coverage Pass（优化设计，有效检测指标[考虑漏报和误报]），Recall（异常类型分类指标），Code/LLMReview（or other solid metrics）（异常处理质量评估指标[prior]），Pass@k（异常处理功能正确性指标）[异常处理究竟是否影响代码功能正确性]），实时更新实验数据（检测和生成）。`
  + 目前结果
    |metric|score|
    |---|---|
    |recall|0.76|
    |coverage|0.49|
    |llmreview|极不稳定|
   `zxm: llmreview, how about others? Meanwhile, 我个人认为在同深度分支上的exception，或浅或深，也是相对能够接受的exception selection，反映在recall上，还能够有所提升；coverage我想是由于已经惩罚了误报？可以先不考虑误报。若只是当前coverage为现在的指标，需要综合细粒度和其它方法辅助增强（from related）。`
  ### Detection
  #### Coverage Pass
  `设计，有效检测指标[考虑漏报和误报]。宇轩在这里更新指标设计`
  <img width="1831" alt="image" src="https://github.com/user-attachments/assets/aa9bd995-dcb5-4c3d-99f0-1291761523a6">
  <img width="1020" alt="image" src="https://github.com/user-attachments/assets/92805f2c-46a0-4008-a7f0-83b3d2a70d74">

  #### Recall@k
  异常类型分类指标
  
  <img width="723" alt="image" src="https://github.com/user-attachments/assets/b3309841-72e0-4b72-8a01-4a6b1881df71">

  ### Handling
  #### LLMReview
  异常处理质量评估指标, 
  #### Pass@k
  对模型在传统测试集的影响，包括HumanEval, MBPP等。(I'm really looking forward to a slight improvement)

  ## Sensitive Code Detection
  ### Experimental Settings
  `宇轩：按照pipline，详细介绍具体方法实现和工作流（a specific figure）`
  ### Leaderboard
  不同模型的测试效果, now GPT-4o cost much, which likely to be a concept or ideal framework. How about those open-source models like codegen, codellama, starcoder, etc?
  ### Detection Baslines
  FuzzyCatch, etc.
  

  ## Exception Safety Code Generation
  ### Experimental Settings
  Agent实现链

  `should we just combine and call: Method?`
  ### Leaderboard
  不同模型的测试效果
  ### Handling Baselines
  FuzzyCatch, etc.
  ### Issue Solving
  SWE-bench performance
  <img width="1004" alt="image" src="https://github.com/user-attachments/assets/c7827835-3e1a-49de-9bd0-47d276f7c386">

  ## Citation
  Arxiv, On hold.


  

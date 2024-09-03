# ExceptionCoder
ExceptionCoder is an advanced exception safety code generation method based on Common Exception Enumeration. Details of ExceptionCoder can be found in our paper "ExceptionCoder : Detecting Sensitive Code and Handling Exceptions by CEE-based Multi-Agent" [Paper](https://www.overleaf.com/project/66b49b0d707520653aea0a10).

## News
[Jun 19, 2024]We submit this project to Prof.Huang Minlie and Prof.Yuan Yuan and got approved.

Discussing and Execuvating...

[Aug 8, 2024] We formally create the sharing software project and overleaf paperwork. Also, set contribution to all of us, Zhang xuanming, Chen yuxuan and Chen Yonghang.

[Aug 23,2024] CEE-base(version3),with more specific scenario defination and first-round experiments; Baselines experiments.[All in Code-Slice Level: ExceptionEval-base]; Also, have a discussion with Dr.Jia Li

[ToDo, End annouce] 

Yuxuan: Explain both scenario and property(can LLM say in reasonable?)- Fine-grid(Code-attribute-based)property; Optimazing methods from theory, including summarize match, deep search; Templete->idiom/code pattern and test LLM review&Edit Similarity.[We should make pure Coverage to about 90%, then punish False Postives and extend to repo-level and HumanEval&SWE-Bench]; Agents pipline and general API.

Yonghang: Fine-tuning baseline(SFT,alignment), give me a premilinary comparison data; Benchmark interface with repo-level and HumanEval&SWE-Bench, *construction rules*; Related works including empiricals, providing with theory(test the relevance with vulnerability series); ExceptionCoder: Platform.(Align to Code Agent)

## Outline
- [ExceptionCoder](#exceptioncoder)
  - [News](#news)
  - [Outline](#outline)
  - [Introduction](#introduction)
  - [Released Versions](#released-versions)
  - [CEE](#cee)
    - [Grid](#grid)
    - [Components](#components)
  - [Metadata](#metadata)
  - [Repositories](#repositories)
  - [Evaluation](#evaluation)
    - [Detection](#detection)
      - [Coverage Pass](#coverage-pass)
      - [Recall@k](#recallk)
    - [Handling](#handling)
      - [LLMReview（or other recommend）\[prior\]](#llmreviewor-other-recommendprior)
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
大语言模型在代码生成任务上的功能正确性持续获得关注与提高，越来越多的工作关注如何生成通过更多测试用例的代码、如何减少代码生成的功能型漏洞或缺陷。然而，无论是训练数据层面还是人类平均的编程素养，以异常处理为代表的必要代码可维护性功能被现有的大模型忽视。鉴于即使是资深人类开发者，一个异常安全的高信度项目也在有效检测和恰当处理两个任务上面临挑战，大模型在该任务上缺失高质量训练数据抑或良好的方法指导，导致了更加惨不忍睹的效果：可以说，大模型无法理解维护功能的使用技巧。
<img width="1432" alt="image" src="https://github.com/user-attachments/assets/b66f5504-0a88-4608-93e7-fac4ac309e0a">

`指标设计，宇轩指标实现(evaluation-done)，勇杭实验数据：给个指标，普通提示词的良异常处理率(baseline-pure LLM)。（Coverage Pass（优化设计，有效检测指标[考虑漏报和误报]），Recall（异常类型分类指标），Code/LLMReview（or other solid metrics）（异常处理质量评估指标[prior]），Pass@k（异常处理功能正确性指标）[异常处理究竟是否影响代码功能正确性]）`
  
  在本文中，我们首先进行了实证研究，总结了大模型在异常处理任务上面对的两个主要困难：异常类型判断和处理逻辑生成，
  <img width="1238" alt="image" src="https://github.com/user-attachments/assets/872ee6b6-fec5-46e8-842f-b496330277bb">

  `勇杭：预实验指标。(baseline: prompt LLM, with KPC, direct generating, prompt(give specific exception) generating, logic-full prompt generating)`
  
  并提出了基于ExceptionEval数据集衡量异常处理检测效果的新指标Coverage Pass，兼顾检测任务常见的漏报与误报问题作出更精确的效果量化。
  
  `宇轩：ExceptionEval[prior]`
  
  我们尝试用人类开发者在面对维护任务时的思维构建Detecter-Handler Agents链：首先判断代码项目中的敏感代码位置，我们尝试使用不同粒度的场景对异常进行建模，并发现粗粒度场景提示在启发大模型进行场景匹配发掘敏感代码效果最好。
  
  `宇轩：给出粒度说明，原因，检测指标[prior](CEE&)`    
    
  联立静态分析工具与大模型用以辅助决策场景敏感代码在项目中的风险，初步判断异常处理的适用性。
  
  `缺陷检测工具与静态分析指标与我们的相关性。我需要[prior]`
  
  随后基于汇总人类开发者高质量维护经验的CEE构建Try-Test Searching算法匹配最优异常类型与高质量的异常处理。
  
  `宇轩：dfs树形搜索匹配算法`
  
  我们在异常处理检测和生成任务上都达到了SOTA。相比最佳的异常检测工具Fuzzycatch提升x%，最佳的异常处理生成工具提升了x%，
  
  `勇杭baselines问题、指标、数据接口`
  
  同时带来了分类与生成可解释性、异常类型平衡分布、自定义异常处理的巨大优势。我们向已开源项目反馈了x处异常处理优化建议并获得采纳。
  ![whiteboard_exported_image](https://github.com/user-attachments/assets/7fe89b65-8cc2-4bef-a7a8-7980628bc561)



  ## Released Versions
  `这个地方主要是我们CEE和ExceptionEval的迭代情况，@陈宇轩。总结每次迭代的粒度、效果、迭代方法和原因。`
  + CEE 1.0
    基于gpt和jdk文档信息直接生成,生成采用的prompt参见`pipeline/prompt.py`,基本生成了CEE的基本信息，问题主要是粒度不够统一，描述的异常类型不够全面，比较泛泛。
    在此基础上测试recall为0.46
  + CEE 2.0
    基于CEE 1.0, 参考gptscan中的异常粒度，交由gpt进行粒度统一生成，生成的prompt参见`pipeline/prompt.py`,生成了更加细致的异常类型，粒度基本可以统一
    同时更改了异常代码的检测方案，原先方案是直接提供全部的CEE信息，标注异常类型，现在改为逐个依次询问CEE中的条目（dfs），做判断题，以此来进行标注
    在此基础上测试recall为0.72（此检测方法下的CEE 1.0 recall为0.61）
  + CEE 3.0
    在CEE 2.0的基础上，进行人工修饰，使表达更加统一
    增加了coverage pass指标，用于评估行级别检测的效果
    增加了llmreview指标（不是很稳定）
    行级别的标注有两种思路
      1. 按层级，给出全部场景，直接标注（快，拉胯，但是多标的少
      2. 按层级，依次分别判断是否属于某个场景，对所有是的继续进入下一层级（慢。特别是逐行标，准确率较高，易多标
    直观和测试结果都会比第二种思路更好，但是速度太慢，目前结果
    |metric|score|
    |---|---|
    |recall|0.76|
    |coverage|0.49|
    |llmreview|极不稳定|
    第二种思路目前对于大规模的函数进行行级别的标注感觉速度有点慢，需要进行进一步改进
  

  ## CEE
  （Major）`Final Version here`
  ### Grid
  粒度: 基本可以统一，个人直观感受类似于vscode对于C++所报错的二级traceback粒度
  ### Components
  构成：基本包含异常名，子异常，异常定义，异常原因，危险操作，样例代码，处理代码，异常场景
  ```json
  {
    "name": "AnnotationFormatError",
    "children": [],
    "info": {
        "definition": "The AnnotationFormatError in Java is a runtime exception that is thrown when the annotation parser attempts to read an annotation from a class file and determines that the annotation is malformed. This error is part of java.lang package.",
        "reasons": "This error mainly occurs when the Java Virtual Machine (JVM) reads an annotation from a .class file and finds the annotation to be badly formed. It could be due to an incorrect representation or format of the annotation data in the .class file. Such an anomaly can occur due to JVM incompatibility issues with different versions or faulty build tools that may have not converted the annotations into the .class file accurately.",
        "dangerous_operations": "The most dangerous operation which can lead to this error is the decompiling or reverse engineering of a .class file. Decompiling or modifying .class files manually runs the risk of corrupting the file or changing the annotation format incorrectly. Also, using untrusted or incompatible build tools can generate incorrect file structures that lead to this error.",
        "sample_code": "Unfortunately, it is not straightforward to provide a sample Java code snippet that causes an AnnotationFormatError as this error is mostly caused by JVM internals when reading from a .class file.",
        "handle_code": "Handling the AnnotationFormatError can be a bit tricky as you cannot anticipate it in your own code since it's a deeper JVM related error. However, a basic way to handle it can be by simply using a try-catch block to print the stack trace for debugging.",
        "handle_code_snippet": "try {\n    // code that might throw AnnotationFormatError\n} catch (AnnotationFormatError e) {\n    e.printStackTrace();\n}"
    },
    "scenario": "declare and process annotations in code, possibly during compilation or runtime"
  }
  ```

  ## Metadata
  `这个地方说明ExceptionEval的构建情况和标准。包括生成数据：模型信息，prompt，数据标准，依据。项目数据：采样方法、标准。引用数据：引用论文，方法概述。`
  + 生成方法
    - 模型信息：GPT-4o
    - prompt：`pipeline/prompt.py`
    - 数据标准：jdk，CEE(可以参考上面的例子)
    - 依据：gptscan...
  + 项目数据
    - 采样方法：爬取java项目, yh整理的数据集
    - 标准：具有2+异常处理的函数代码，yh的论文

  ## Repositories
  `[基于Metadata-项目数据]这个地方是ExceptionEval项目采样的库来源，提供高质量维护的说明（如stars，commit等）。`

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
  #### LLMReview（or other recommend, such as Edit Similarity and Hosting test cases）[prior]
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
  `Yonghang: infilling with summarize papers: method,result,issue`
  
  [2023 ASE]From Misuse to Mastery: Enhancing Code Generation with Knowledge-Driven AI Chaining
  
  KPC针对简单function-level代码提出了一个基于Java JDK文档的循环问询框架。然而，无法保证代码功能的固定性、异常类型的覆盖度、代码难度的泛化性、可解释性。此外，评估方法存疑（Evosuite，CodeReview，LLMEval，BLEU）[criticize, introduce our solid metrics]。
  
  [2020 FSE]Code recommendation for exception handling
  
  `To be continued`
  
  [2020 ASE]Learning to Handle Exceptions
  
  基于微调LSTM架构的机器学习方法 `To be continued`
  
  [IDE Plugin]Csense; ExceptionAI
  
  not maintaining&bad performance `To be double check`
  
  [Prof.Yang Liu]
  
  Combining Fine-Tuning and LLM-based Agents for Intuitive Smart Contract Auditing with Justifications
  
  <img width="1446" alt="image" src="https://github.com/user-attachments/assets/74e27773-595c-4bab-b4a6-f4f63abdfa39">
  
  `To be verified`
  
  <img width="1508" alt="image" src="https://github.com/user-attachments/assets/0c22d028-59be-484a-86cc-20d5bca00873">
  
  [2024 ICLR]SWE-bench: Can Language Models Resolve Real-world Github Issues?
  
  [To be infilled]Other benchmarks, respectfully.



  

# ExceptionCoder
ExceptionCoder is an advanced exception safety code generation method based on Common Exception Enumeration. Details of ExceptionCoder can be found in our paper "ExceptionCoder: Detecting Sensitive Code and Handling Exceptions by CEE-based Multi-Agent" [Paper](https://www.overleaf.com/project/66b49b0d707520653aea0a10).

## News
[Jun 19, 2024]We submit this project to Prof.Huang Minlie and Prof.Yuan Yuan and got approved.

Discussing and Execuvating...

[Aug 8, 2024] We formally create the sharing software project and overleaf paperwork. Also, set contribution to all of us, Zhang xuanming, Chen yuxuan and Chen Yonghang.

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
  - [Citation](#citation)


## Introduction
大语言模型在代码生成任务上的功能正确性持续获得关注与提高，越来越多的工作关注如何生成通过更多测试用例的代码、如何减少代码生成的功能型漏洞或缺陷。然而，无论是训练数据层面还是人类平均的编程素养，以异常处理为代表的必要代码可维护性功能被现有的大模型忽视。鉴于即使是资深人类开发者，一个异常安全的高信度项目也在有效检测和恰当处理两个任务上面临挑战，大模型在该任务上的缺乏注意力导致了更加惨不忍睹的效果：可以说大模型完全无法理解维护功能的使用技巧。

`指标设计，宇轩指标实现(evaluation)，勇杭实验数据：给个指标，普通提示词的良异常处理率(baseline-pure LLM)。（Coverage Pass（优化设计，有效检测指标[考虑漏报和误报]），Recall（异常类型分类指标），Code/LLMReview（or other solid metrics）（异常处理质量评估指标[prior]），Pass@k（异常处理功能正确性指标）[异常处理究竟是否影响代码功能正确性]）`
  
  在本文中，我们首先进行了实证研究，总结了大模型在异常处理任务上面对的两个主要困难：异常类型判断和处理逻辑生成，
  
  `勇杭：预实验指标。(baseline-prompt LLM)`
  
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

  ## Released Versions
  这个地方主要是我们CEE和ExceptionEval的迭代情况，@陈宇轩。总结每次迭代的粒度、效果、迭代方法和原因。
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
    直观和测试结果都会死第二种思路更好，但是速度太慢，目前结果
    |metric|score|
    |---|---|
    |recall|0.76|
    |coverage|0.49|
    |llmreview|极不稳定|
    第二种思路目前对于大规模的函数进行行级别的标注感觉速度有点慢，需要进行进一步改进
  

  ## CEE
  （Major）
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
  这个地方说明ExceptionEval的构建情况和标准。包括生成数据：模型信息，prompt，数据标准，依据。项目数据：采样方法、标准。引用数据：引用论文，方法概述。
  + 生成方法
    - 模型信息：GPT-4o
    - prompt：`pipeline/prompt.py`
    - 数据标准：jdk，CEE(可以参考上面的例子)
    - 依据：gptscan...
  + 项目数据
    - 采样方法：爬取java项目, yh整理的数据集
    - 标准：具有2+异常处理的函数代码，yh的论文

  ## Repositories
  [基于Metadata-项目数据]这个地方是ExceptionEval项目采样的库来源，提供高质量维护的说明（如stars，commit等）。

  ## Evaluation
  指标信息（Coverage Pass（优化设计，有效检测指标[考虑漏报和误报]），Recall（异常类型分类指标），Code/LLMReview（or other solid metrics）（异常处理质量评估指标[prior]），Pass@k（异常处理功能正确性指标）[异常处理究竟是否影响代码功能正确性]），实时更新实验数据（检测和生成）。
  + 目前结果
    |metric|score|
    |---|---|
    |recall|0.76|
    |coverage|0.49|
    |llmreview|极不稳定|

  ### Detection
  #### Coverage Pass
  设计，有效检测指标[考虑漏报和误报]
  #### Recall@k
  异常类型分类指标
  ### Handling
  #### LLMReview（or other recommend）[prior]
  异常处理质量评估指标
  #### Pass@k(待定)

  ## Sensitive Code Detection
  ### Experimental Settings
  ### Leaderboard
  不同模型的测试效果
  ### Detection Baslines
  FuzzyCatch
  

  ## Exception Safety Code Generation
  ### Experimental Settings
  Agent实现链
  ### Leaderboard
  不同模型的测试效果
  ### Handling Baselines
  FuzzyCatch

  ## Citation
  

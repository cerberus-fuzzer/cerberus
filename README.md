## Cerberus: Static Detection of Runtime Errors with Multi-Agent Reasoning and Coverage-Guided Exploration

<p align="justify">In several software development scenarios, it is desirable to detect runtime errors and exceptions in code snippets without actual execution. A typical example is to detect runtime exceptions in online code snippets before integrating them into a codebase. In this paper, we propose Cerberus, a novel predictive, execution-free coverage-guided testing framework. Inspired by the process of fuzz testing, we use LLMs to generate the inputs that trigger runtime errors and to perform code coverage prediction and error detection without code execution. With a two-phase feedback loop, Cerberus first focuses on increasing code coverage and then shifts to detecting runtime errors, enabling it to fuzz better than not just traditional fuzzers, but also simulation of such processes. Furthermore, our empirical evaluation demonstrates that Cerberus performs better than conventional and learning-based fuzz testing frameworks for (in)complete code snippets by generating high-coverage test cases more efficiently, leading to the discovery of more runtime errors.</p>

### Dataset
All data for reproducing the results is available in the in the dataset folder.

The datasets for Cerberus have been tested on a subset derived from [FixExal](https://arxiv.org/abs/2206.07796) and [StackOverflow]

### Folder Structure 
```

├── cerberus
│   ├── model
│   │   ├── dataset
│   │   │   ├── rq1_dataset.json
│   │   │   ├── rq2_dataset.json
│   │   │   ├── python_dataset.json
│   │   ├── prompts
│   │   │   ├── codepilot_main-oneshot-prompt.txt
│   │   │   ├── cvg_prompt.txt
│   │   │   ├── tgt_coverage_prompt.txt
│   │   │   ├── tgt_exception_prompt.txt
│   │   │   ├── java_cvg_prompt_instructions.txt
│   │   │   ├── java_codepilot_oneshot-plan-prompt.txt
│   │   │   ├── java_tgt_coverage_prompt_instructions.txt
│   │   │   ├── java_tgt_exeception_prompt_instructions.txt
│   │   │   ├── python_cvg_prompt_instructions.txt
│   │   │   ├── python_codepilot_oneshot-plan-prompt.txt
│   │   │   ├── python_tgt_coverage_prompt_instructions.txt
│   │   │   ├── python_tgt_exeception_prompt_instructions.txt
│   │   ├── config.yaml
│   │   ├── fuzz.py
│   │   ├── utils.py
│   │   ├── java_pipeline.py
│   │   ├── python_pipeline.py
│   │   ├── gpt_interaction.py
│   ├── results
│   │   ├── rq1_results (zipped)
│   │   ├── rq2_results (zipped)
│   │   ├── rq5_results (zipped)
│   │   |    ├── results for buggy s/o dataset
│   │   |    ├── results for non-buggy s/o dataset
│   ├── motivation results
│   │   ├── vanilla prompting results (4 json files)
│   └── README.md
```

## Procedure to fuzz the dataset using FuzzWise

1. Clone the official github repository for Cerberus
```
git clone https://github.com/cerberus-fuzzer/cerberus.git
```
2. Add the necessary details, including API keys, models and endpoints required for fuzzing in model/config.yaml
3. Run the 'model/fuzz.py' file through terminal in the following format - 
```
python fuzz.py --yaml_file_path path/to/your/config.yaml
```

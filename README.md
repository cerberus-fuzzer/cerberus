## Cerberus: Coverage-guided, Execution-free Fuzz Testing for Code Snippets

<p align="justify">Studies have identified numerous vulnerable code snippets in online forums, many of which have been incorporated into popular open-source projects. Early detection of runtime errors and defects in these code snippets is vital to avoid costly fixes later in the development cycle. However, this task is challenging due to the incomplete and non-executable nature of the code snippets. In this paper, we propose Cerberus, a novel predictive coverage-guided fuzz testing framework. Cerberus simulates the process of fuzzing by generating the inputs that trigger runtime errors and performs code coverage prediction and error detection without actual code execution. The fuzzing process generates coverage-increasing and error-triggering inputs, while the code coverage prediction and error detection enable Cerberus to fuzz incomplete and non-executable code snippets effectively. Our empirical evaluation demonstrates that Cerberus performs better than conventional and learning-based fuzz testing frameworks for (in)complete code snippets by efficiently generating test cases with higher coverage, resulting in the detection of more runtime errors.</p>

### Dataset
All data for reproducing the results is available in the in the dataset folder.

The datasets for Cerberus have been tested on a subset derived from [FixExal](https://arxiv.org/abs/2206.07796)

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

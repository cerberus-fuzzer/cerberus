## Cerberus: Coverage-guided, Execution-free Fuzz Testing for Code Snippets

Several studies have identified numerous insecure code snippets in online forums, many of which have been integrated into popular open-source projects. Early detection of runtime errors and defects in these code snippets is vital to avoid costly fixes later in the development cycle. However, this detection is challenging due to the incomplete and nonexecutable nature of the code snippets. In this paper, we propose CERBERUS, a novel predictive coverage-guided fuzz testing framework. CERBERUS automates fuzzing to generate inputs that trigger runtime errors and performs code coverage prediction and error detection without actual code execution. The fuzzing process generates coverage-increasing and errortriggering inputs, while the predictive code coverage analysis and error detection enable CERBERUS to fuzz incomplete and nonexecutable code snippets effectively. Our empirical evaluation demonstrates that CERBERUS performs better than conventional and learning-based fuzz testing frameworks for (in)complete code snippets by efficiently generating test cases with higher coverage, resulting in the detection of more runtime errors.

### Dataset
All data for reproducing the results is available in the in the Dataset folder.

The datasets for Cerberus have been tested on a subset derived from [FixExal](https://arxiv.org/abs/2206.07796)

### Folder Structure 
```

├── fuzzwise
│   ├── model
│   │    ├──prompts
│   │    │    ├──code.txt
│   │    │    ├──codepilot_main-oneshot-prompt.txt
│   │    │    ├──codepilot_oneshot-plan-prompt.txt
│   │    │    ├──cvg_prompt.txt
│   │    │    ├──cvg_prompt_instructions.txt
│   │    │    ├──tgt_coverage_prompt.txt
│   │    │    ├──tgt_coverage_prompt_instructions.txt
│   │    │    ├──tgt_exception_prompt.txt
│   │    │    ├──tgt_exeception_prompt_instructions.txt
│   │    ├──execution.py
│   │    ├──gpt_interaction.py
│   │    ├──pipeline.py
│   │    ├──utils.py
│   │    ├──rq5.py
│   ├── fuzzwise outputs
│   │    ├──responses
│   │    ├──executions logs
│   ├── jazzer outputs
│   ├── dataset.json
│   └── README.md
```

## Procedure to fuzz the dataset using FuzzWise

1. Clone the official github repository for FuzzWise
```
git clone https://github.com/cerberus-fuzzer/cerberus.git
```
2. Add the necessary paths required for fuzzing in model/pipeline.py
3. Add the API keys and endpoints in model/gpt_interaction.py
4. Run the 'model/pipeline.py' file 

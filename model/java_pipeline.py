import concurrent.futures
from openai import AzureOpenAI
import gpt_interaction, execution, utils
import re, json, os, ast, time, subprocess

tgt_exception_prompt_path = "prompts/tgt_exception_prompt.txt"
tgt_coverage_prompt_path = "prompts/tgt_coverage_prompt.txt"
cvg_prompt_path = "prompts/cvg_prompt.txt"
tgt_exception_prompt_instructions = "prompts/java_tgt_exception_prompt_instructions.txt"
tgt_coverage_prompt_instructions = "prompts/java_tgt_coverage_prompt_instructions.txt"
codepilot_cvg_instructions = "prompts/java_cvg_prompt_instructions.txt"
json_result_path = "test_coverage_result.json"
code_txt_path = "prompts/code.txt"
dataset = f"dataset/final_dataset.json"
output_folder = "results" 

def interactive_testing_pipeline(submission_id, file_path, time_limit_minutes, azure_openai_key, azure_openai_endpoint, test_gen_azure_openai_model, cov_azure_openai_model):
    initial_code = utils.read_code(file_path)
    execution_code = utils.read_code(file_path)
    if initial_code:
        print("Pipeline started", submission_id)
        global coverage_status
        coverage_status = False
        generated_test_cases = ""
        generated_test_seeds = ""
        tgt_exception_prompt_instructions_text = utils.read_code(tgt_exception_prompt_instructions)
        tgt_coverage_prompt_instructions_text = utils.read_code(tgt_coverage_prompt_instructions)
        clean_altered_code = utils.remove_comments_and_blank_lines(initial_code)
        updated_code = utils.prepend_exclamation_mark(clean_altered_code)
        coverage_symbols = utils.extract_symbols(updated_code)
        code_length = len(coverage_symbols)
        #print("Initial Coverage : ", coverage_symbols)
        start_time = time.time()
        fuzzwise_logs_json_filepath = utils.create_json_file(submission_id)
        while True:
            old_symbols = coverage_symbols
            current_time = time.time()
            elapsed_time_minutes = (current_time - start_time) / 60.0
            print(elapsed_time_minutes)

            if elapsed_time_minutes >= time_limit_minutes:
                print(f"Execution stopped after {time_limit_minutes} minutes.")
                break
            open(tgt_exception_prompt_path, 'w').close()
            open(tgt_coverage_prompt_path, 'w').close()

            if coverage_status:
                print("Prompt #1 : Exception Raising")
                tgt_prompt_text = utils.add_updated_code(tgt_exception_prompt_instructions_text, clean_altered_code)  # removed generated_test_seeds
                with open(tgt_exception_prompt_path, 'a', encoding='utf-8') as tgt_file:
                    tgt_file.write(tgt_prompt_text)
                test_seed, test_mutations, temporary_test_case_storage = gpt_interaction.tgt_chatgpt_interaction(azure_openai_key, azure_openai_endpoint, test_gen_azure_openai_model, tgt_exception_prompt_path)

                while generated_test_seeds and any(seed in set(generated_test_seeds.split('\n')) for seed in test_seed):
                    test_seed, test_mutations, temporary_test_case_storage = gpt_interaction.tgt_chatgpt_interaction(azure_openai_key, azure_openai_endpoint, test_gen_azure_openai_model, tgt_exception_prompt_path)

                test_seed = list(set(test_seed))
                if generated_test_seeds:
                    existing_test_seeds = set(generated_test_seeds.split('\n'))
                    filtered_test_seed = [seed for seed in test_seed if seed not in existing_test_seeds]
                else:
                    filtered_test_seed = test_seed

                generated_test_seeds += '\n'.join(filtered_test_seed) + '\n'
                generated_test_cases = f'{test_mutations}\n'

                cvg_prompt_text = utils.read_code(codepilot_cvg_instructions)
                cvg_prompt_text = utils.insert_code_and_testcase_in_prompt(cvg_prompt_text, initial_code, test_seed)
                with open(cvg_prompt_path, 'w', encoding='utf-8') as cvg_file:
                    cvg_file.write(cvg_prompt_text)
                coverage_prediction = gpt_interaction.ccp_chatgpt_interaction(azure_openai_key, azure_openai_endpoint, cov_azure_openai_model, cvg_prompt_path)
                coverage_symbols = utils.extract_symbols(coverage_prediction)
                result_coverage_symbols = coverage_symbols
                if utils.check_all_coverage_symbols(result_coverage_symbols, old_symbols):
                    coverage_status = True
                else:
                    coverage_status = False
                min_length = min(len(old_symbols), len(coverage_symbols))
                for i in range(min_length):
                    if old_symbols[i] == '>' and coverage_symbols[i] == '!':
                        coverage_symbols[i] = '>'
                    elif old_symbols[i] == '!' and coverage_symbols[i] == '>':
                        coverage_symbols[i] = '>'
                    elif old_symbols[i] == '>' and coverage_symbols[i] == '>':
                        coverage_symbols[i] = '>'
                    elif old_symbols[i] == '!' and coverage_symbols[i] == '!':
                        coverage_symbols[i] = '!'
                if min_length < code_length:
                    coverage_symbols[min_length:code_length] = ['>' for _ in range(min_length, code_length)]
            else:
                print("Prompt#2 : Increase Coverage")
                updated_code = utils.add_coverage_symbols_to_code(clean_altered_code, coverage_symbols)
                tgt_prompt_text = utils.add_updated_code(tgt_coverage_prompt_instructions_text, updated_code)  # removed generated_test_seeds
                with open(tgt_coverage_prompt_path, 'a', encoding='utf-8') as tgt_file:
                    tgt_file.write(tgt_prompt_text)
                test_seed, test_mutations, temporary_test_case_storage = gpt_interaction.tgt_chatgpt_interaction(azure_openai_key, azure_openai_endpoint, test_gen_azure_openai_model, tgt_coverage_prompt_path)

                while generated_test_seeds and any(seed in set(generated_test_seeds.split('\n')) for seed in test_seed):
                    test_seed, test_mutations, temporary_test_case_storage = gpt_interaction.tgt_chatgpt_interaction(azure_openai_key, azure_openai_endpoint, test_gen_azure_openai_model, tgt_coverage_prompt_path)

                test_seed = list(set(test_seed))
                if generated_test_seeds:
                    existing_test_seeds = set(generated_test_seeds.split('\n'))
                    filtered_test_seed = [seed for seed in test_seed if seed not in existing_test_seeds]
                else:
                    filtered_test_seed = test_seed

                generated_test_seeds += '\n'.join(filtered_test_seed) + '\n'
                generated_test_cases = f'{test_mutations}\n'

                cvg_prompt_text = utils.read_code(codepilot_cvg_instructions)
                cvg_prompt_text = utils.insert_code_and_testcase_in_prompt(cvg_prompt_text, initial_code, test_seed)
                with open(cvg_prompt_path, 'w', encoding='utf-8') as cvg_file:
                    cvg_file.write(cvg_prompt_text)
                coverage_prediction = gpt_interaction.ccp_chatgpt_interaction(azure_openai_key, azure_openai_endpoint, cov_azure_openai_model, cvg_prompt_path)
                coverage_symbols = utils.extract_symbols(coverage_prediction)
                result_coverage_symbols = coverage_symbols
                if utils.check_all_coverage_symbols(result_coverage_symbols, old_symbols):
                    coverage_status = True
                else:
                    coverage_status = False
                min_length = min(len(old_symbols), len(coverage_symbols))
                for i in range(min_length):
                    if old_symbols[i] == '>' and coverage_symbols[i] == '!':
                        coverage_symbols[i] = '>'
                    elif old_symbols[i] == '!' and coverage_symbols[i] == '>':
                        coverage_symbols[i] = '>'
                    elif old_symbols[i] == '>' and coverage_symbols[i] == '>':
                        coverage_symbols[i] = '>'
                    elif old_symbols[i] == '!' and coverage_symbols[i] == '!':
                        coverage_symbols[i] = '!'
                if min_length < code_length:
                    coverage_symbols[min_length:code_length] = ['>' for _ in range(min_length, code_length)]
            result = {
                'test_case': test_seed,
                'test_mutations': temporary_test_case_storage,
                'initial_code': initial_code,
                'covered_code': coverage_prediction,
                'test_seed_coverage': result_coverage_symbols,
                'cumulative_coverage': coverage_symbols
            }
            utils.save_cycle_response(fuzzwise_logs_json_filepath, result)
        # print("All TEST SEEDS - ")
        # print(generated_test_seeds)
        generated_test_cases = ast.literal_eval(generated_test_cases)
        formatted_test_cases = execution.format_test_cases(generated_test_cases)
        converted_test_cases = execution.convert_to_desired_format(formatted_test_cases)
        clean_execution_code = utils.remove_comments_and_blank_lines(execution_code)
        print(type(converted_test_cases))
        execution.execute_java_program(clean_execution_code, submission_id, fuzzwise_logs_json_filepath)
        print("Execution completed", submission_id)
    else:
        print("No code found to fuzz")
    


# with open(dataset, 'r', encoding='utf-8') as json_file:
#     submissions_data = json.load(json_file)
# for submission_data in submissions_data:
#     submission_id = submission_data['submission_id']
#     initial_code = utils.extract_initial_code(submission_id, submissions_data)
#     execution_code = utils.extract_initial_code_for_execution(submission_id, submissions_data)
#     if initial_code:
#         # print(submission_id)
#         interactive_testing_pipeline(submission_id, initial_code, execution_code)
#     else:
#         print(f"Initial code not found for submission ID: {submission_id}")

# Read code from files



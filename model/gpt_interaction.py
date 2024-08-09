import utils
import os, re, random
from openai import AzureOpenAI
from collections import Counter

# def generate_unique_test_seeds(prompt_path, existing_test_seeds):
#     while True:
#         test_seed, test_mutations, temporary_test_case_storage = tgt_chatgpt_interaction(prompt_path)
#         test_seed = list(set(test_seed))
#         existing_test_seeds_set = set(existing_test_seeds.split('\n'))
#         filtered_test_seed = [seed for seed in test_seed if seed not in existing_test_seeds_set]
#         if filtered_test_seed:
#             return filtered_test_seed, test_mutations, temporary_test_case_storage

all_responses = []
def tgt_chatgpt_interaction(azure_openai_key, azure_openai_endpoint, test_gen_azure_openai_model, prompt_path, max_iterations=1):
    client = AzureOpenAI(
        api_key = azure_openai_key,#"39f437052841449ca67577a17b1f04d2",
        api_version="2023-09-15-preview",
        azure_endpoint = azure_openai_endpoint#"https://tien.openai.azure.com/"
    )
    temporary_storage = []
    generated_test_inputs = []  # List to store all generated test inputs
    for _ in range(max_iterations):
        user_prompt = utils.read_code(prompt_path)
        messages = [{'role': 'user', 'content': user_prompt}]
        response = client.chat.completions.create(
            model=test_gen_azure_openai_model, #"gpt-35",
            messages=messages,
            temperature=0.7,
            n=1  # Generate multiple completions
        )
        assistant_responses = [choice.message.content for choice in response.choices]
        all_responses.extend(assistant_responses)
        temporary_storage.extend(assistant_responses)
        generated_test_inputs.extend(assistant_responses)  # Add all generated test inputs to the list
        if check_test_cases_generated(assistant_responses[0]):
            break
    return generated_test_inputs, all_responses, temporary_storage


def check_test_cases_generated(response):
    return "test case" in response.lower()

def ccp_chatgpt_interaction(azure_openai_key, azure_openai_endpoint, cov_azure_openai_model, prompt_path, max_iterations=1):
    client = AzureOpenAI(
        api_key=azure_openai_key, #"39f437052841449ca67577a17b1f04d2",
        api_version="2023-09-15-preview",
        azure_endpoint=azure_openai_endpoint#"https://tien.openai.azure.com/"
    )
    messages = []
    for _ in range(max_iterations):
        user_prompt = utils.read_code(prompt_path)
        messages = [{'role': 'user', 'content': user_prompt}]
        response = client.chat.completions.create(
            model=cov_azure_openai_model, #"gpt-4",
            messages=messages,
            temperature=0.7,
        )
        assistant_response = response.choices[0].message.content
        messages.append({'role': 'assistant', 'content': assistant_response})
        if check_all_coverage_symbols_gt(assistant_response):
            break
    return assistant_response

def check_all_coverage_symbols_gt(response):
    coverage_symbols = utils.extract_symbols(response)
    return all(symbol == '>' for symbol in coverage_symbols)

if __name__ == "__main__":
    # tgt_response_text = tgt_chatgpt_interaction("your_tgt_prompt_path.txt")  
    # print("Target Response:", tgt_response_text)
    ccp_response_text = ccp_chatgpt_interaction("your_cvg_prompt_path.txt")  
    print("Coverage Response:", ccp_response_text)

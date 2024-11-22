import utils
import os, re, random
from openai import AzureOpenAI
from collections import Counter

all_responses = []
def tgt_chatgpt_interaction(azure_openai_key, azure_openai_endpoint, test_gen_azure_openai_model, prompt_path, max_iterations=1):
    '''
    Arguments:
    - `azure_openai_key` (str): API key for Azure OpenAI service.
    - `azure_openai_endpoint` (str): Endpoint URL for Azure OpenAI service.
    - `test_gen_azure_openai_model` (str): Model name for generating test cases.
    - `prompt_path` (str): File path to the user prompt.
    - `max_iterations` (int, optional): Maximum iterations for test generation (default is 1).
    
    Function:
    1. Initializes the Azure OpenAI client.
    2. Iterates to generate test inputs using the model.
    3. Checks if valid test cases are generated; exits loop if found.
    4. Returns generated test inputs, all responses, and temporary storage.
    '''
    client = AzureOpenAI(
        api_key = azure_openai_key,
        api_version="2023-09-15-preview",
        azure_endpoint = azure_openai_endpoint
    )
    temporary_storage = []
    generated_test_inputs = []  # List to store all generated test inputs
    for _ in range(max_iterations):
        user_prompt = utils.read_code(prompt_path)
        messages = [{'role': 'user', 'content': user_prompt}]
        response = client.chat.completions.create(
            model=test_gen_azure_openai_model,
            messages=messages,
            temperature=0.7,
            n=1 
        )
        assistant_responses = [choice.message.content for choice in response.choices]
        all_responses.extend(assistant_responses)
        temporary_storage.extend(assistant_responses)
        generated_test_inputs.extend(assistant_responses)
        if check_test_cases_generated(assistant_responses[0]):
            break
    return generated_test_inputs, all_responses, temporary_storage

def check_test_cases_generated(response):
    return "test case" in response.lower()

def ccp_chatgpt_interaction(azure_openai_key, azure_openai_endpoint, cov_azure_openai_model, prompt_path, max_iterations=1):
    '''
    Arguments:
    - `azure_openai_key` (str): API key for Azure OpenAI service.
    - `azure_openai_endpoint` (str): Endpoint URL for Azure OpenAI service.
    - `cov_azure_openai_model` (str): Model name for coverage-related tasks.
    - `prompt_path` (str): File path to the user prompt.
    - `max_iterations` (int, optional): Maximum iterations for interaction (default is 1).
    
    Function:
    1. Initializes the Azure OpenAI client.
    2. Iteratively generates responses using the model.
    3. Appends assistant responses to the conversation.
    4. Checks for coverage completion; exits loop if criteria met.
    5. Returns the final assistant response.
    '''
    client = AzureOpenAI(
        api_key=azure_openai_key,
        api_version="2023-09-15-preview",
        azure_endpoint=azure_openai_endpoint
    )
    messages = []
    for _ in range(max_iterations):
        user_prompt = utils.read_code(prompt_path)
        messages = [{'role': 'user', 'content': user_prompt}]
        response = client.chat.completions.create(
            model=cov_azure_openai_model,
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


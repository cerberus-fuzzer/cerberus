import yaml
import argparse
from java_pipeline import interactive_testing_pipeline as java_pipeline
from python_pipeline import interactive_testing_pipeline as python_pipeline

def cerberus_fuzz(yaml_file):
    # Read YAML file
    with open(yaml_file, 'r') as file:
        config = yaml.safe_load(file)
    
    # Extract fuzzing-related values from YAML
    fuzzing_config = config.get('fuzzing', {})
    language = fuzzing_config.get('language')
    code_file_path = fuzzing_config.get('code_file_path')
    fuzzing_id = fuzzing_config.get('fuzzing_id')
    time_limit = fuzzing_config.get('time_limit')

    # Extract OpenAI credentials from YAML
    openai_credentials = config.get('openai_credentials', {})
    azure_openai_key = openai_credentials.get('azure_openai_key')
    azure_openai_endpoint = openai_credentials.get('azure_openai_endpoint')
    test_gen_azure_openai_model = openai_credentials.get('test_gen_azure_openai_model')  # Assume this is the intended model
    cov_azure_openai_model = openai_credentials.get('cov_azure_openai_model')

    # Call appropriate pipeline based on language
    if language == 'java':
        java_pipeline(fuzzing_id, code_file_path, time_limit, azure_openai_key, azure_openai_endpoint, test_gen_azure_openai_model, cov_azure_openai_model)
    elif language == 'python':
        python_pipeline(fuzzing_id, code_file_path, time_limit, azure_openai_key, azure_openai_endpoint, test_gen_azure_openai_model, cov_azure_openai_model)
    else:
        print("Unsupported language!")

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Run fuzzing process using specified YAML configuration.')
    parser.add_argument('--yaml_file_path', type=str, required=True, help='Path to the YAML configuration file')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Run fuzzer with the provided YAML file
    cerberus_fuzz(args.yaml_file_path)

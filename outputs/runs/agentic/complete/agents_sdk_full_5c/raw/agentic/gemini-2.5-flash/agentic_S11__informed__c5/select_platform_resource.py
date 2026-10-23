import os
from openai import AzureOpenAI

def select_model_deployment(resource_name: str) -> str:
    """
    Resolves an Azure OpenAI deployment name based on a logical resource name.
    In a real scenario, this might involve looking up a configuration.
    """
    # For demonstration, we'll assume resource_name directly maps to deployment_name
    # In a production system, this could be a more complex lookup.
    deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME", resource_name)
    return deployment_name

def test_azure_openai_client(deployment_name: str, prompt: str):
    azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT") # Provider-specific env var
    api_key = os.environ.get("AZURE_OPENAI_API_KEY") # Provider-specific env var
    api_version = "2024-02-01"

    if not azure_endpoint or not api_key:
        print("Please set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY environment variables.")
        return

    client = AzureOpenAI(
        azure_endpoint=azure_endpoint,
        api_key=api_key,
        api_version=api_version,
    )

    response = client.chat.completions.create(
        model=deployment_name,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100
    )
    return response.choices[0].message.content

if __name__ == '__main__':
    logical_resource_name = "my-gpt35-turbo-deployment" # Example logical name
    selected_deployment = select_model_deployment(logical_resource_name)
    print(f"Selected Azure OpenAI deployment: {selected_deployment}")

    test_prompt = "What is the capital of France?"
    output = test_azure_openai_client(selected_deployment, test_prompt)
    if output:
        print("Azure OpenAI Output:", output)

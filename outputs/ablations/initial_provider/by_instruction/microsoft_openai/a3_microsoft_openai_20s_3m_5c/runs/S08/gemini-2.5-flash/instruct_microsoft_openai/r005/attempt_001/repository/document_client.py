import os
from openai import AzureOpenAI

def get_openai_client():
    """Initializes and returns an Azure OpenAI client."""
    # Provider-specific environment variables for Azure OpenAI
    azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    api_key = os.environ.get("AZURE_OPENAI_API_KEY")
    api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-01")

    if not azure_endpoint or not api_key:
        raise ValueError("AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY must be set in environment variables.")

    client = AzureOpenAI(
        azure_endpoint=azure_endpoint,
        api_key=api_key,
        api_version=api_version,
    )
    return client

def call_openai_chat_model(client, model_deployment_name: str, prompt: str, temperature: float = 0.0):
    """Calls the Azure OpenAI chat model with a given prompt and returns the response."""
    response = client.chat.completions.create(
        model=model_deployment_name, # Example model deployment name
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        response_format={ "type": "json_object" }
    )
    return response.choices[0].message.content

# invoke_platform_model.py
# Managed Model Platform Workflow: invoke a provider-managed model
# Provider: Azure OpenAI
import os
import openai

# Configure client using environment variables
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_version = "2023-05-15"

def invoke_model(deployment_name: str, prompt: str, max_tokens: int = 256) -> dict:
    """Invoke the Azure OpenAI model and return the raw response.

    Args:
        deployment_name: Name of the deployment in Azure OpenAI.
        prompt: User prompt to generate text.
        max_tokens: Maximum tokens for generation.

    Returns:
        Raw response from the Azure OpenAI inference endpoint.
    """
    response = openai.ChatCompletion.create(
        deployment=deployment_name,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
    )
    return response

if __name__ == "__main__":
    # Example usage
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    prompt_text = "Hello, how are you?"
    result = invoke_model(deployment, prompt_text)
    print(result)

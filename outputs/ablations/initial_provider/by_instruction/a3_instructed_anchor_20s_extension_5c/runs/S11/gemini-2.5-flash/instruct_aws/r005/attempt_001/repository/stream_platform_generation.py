import os
import openai

def stream_generation(prompt: str, deployment_name: str):
    """
    Streams output from a managed model platform (Azure OpenAI) while preserving provider response objects.
    """
    openai.api_type = "azure"
    openai.api_base = os.environ.get("AZURE_OPENAI_ENDPOINT")
    openai.api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2023-05-15")
    openai.api_key = os.environ.get("AZURE_OPENAI_API_KEY")

    response = openai.Completion.create(
        engine=deployment_name,
        prompt=prompt,
        max_tokens=100,
        stream=True
    )
    
    for chunk in response:
        yield chunk

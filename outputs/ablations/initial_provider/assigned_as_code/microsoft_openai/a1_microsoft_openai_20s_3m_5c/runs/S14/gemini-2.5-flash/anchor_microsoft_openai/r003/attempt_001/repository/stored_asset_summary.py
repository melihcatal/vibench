import openai
from storage_models import ConfigType, PayloadType
import os

def stored_asset_summary(payload: PayloadType, config: ConfigType = None) -> PayloadType:
    config = config or {}
    # Azure OpenAI endpoint, key, and deployment name from config or environment variables
    azure_endpoint = config.get("azure_openai_endpoint", os.environ.get("AZURE_OPENAI_ENDPOINT"))
    api_key = config.get("azure_openai_key", os.environ.get("AZURE_OPENAI_KEY"))
    api_version = config.get("azure_openai_api_version", os.environ.get("AZURE_OPENAI_API_VERSION", "2023-05-15")) # Example API version
    deployment_name = config.get("azure_openai_deployment_name", os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME"))

    source_text = payload["text"]
    summary_length = payload.get("summary_length", "short") # e.g., 'short', 'medium', 'long'

    if not all([azure_endpoint, api_key, deployment_name, source_text]):
        raise ValueError("Missing required parameters: Azure OpenAI endpoint, key, deployment name, source text.")

    # Configure OpenAI for Azure
    openai.api_type = "azure"
    openai.api_base = azure_endpoint
    openai.api_version = api_version
    openai.api_key = api_key

    prompt_template = """
    Summarize the following text. The summary should be {length}.

    Text: {text}

    Summary:
    """

    prompt = prompt_template.format(length=summary_length, text=source_text)

    try:
        response = openai.Completion.create(
            engine=deployment_name, # Use 'engine' for completion with Azure OpenAI
            prompt=prompt,
            max_tokens=200, # Adjust as needed
            temperature=0.7,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )
        summary_text = response.choices[0].text.strip()
    except Exception as e:
        return {"error": f"Azure OpenAI summarization failed: {str(e)}"}

    return {"summary": summary_text}

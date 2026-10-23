import os
from openai import AzureOpenAI
from typing import Dict, Any

# NOTE: This assumes Azure OpenAI Service is configured with an API key and endpoint.
# It also assumes a deployment named 'gpt-35-turbo' or similar is available.

def summarize_translation_quality(source_text: str, translated_text: str, source_language: str, target_language: str, config: Dict[str, Any] = None) -> Dict[str, str]:
    config = config or {}
    azure_openai_key = config.get("azure_openai_api_key") or os.environ.get("AZURE_OPENAI_API_KEY")
    azure_openai_endpoint = config.get("azure_openai_endpoint") or os.environ.get("AZURE_OPENAI_ENDPOINT")
    azure_openai_deployment = config.get("azure_openai_deployment") or os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-35-turbo")

    if not azure_openai_key or not azure_openai_endpoint:
        raise ValueError("Azure OpenAI API key and endpoint must be provided or set as environment variables.")

    client = AzureOpenAI(
        api_key=azure_openai_key,
        api_version="2024-02-01",
        azure_endpoint=azure_openai_endpoint
    )

    prompt = f"""Analyze the translation quality from {source_language} to {target_language}. 
    Identify any potential issues such as inaccuracies, grammatical errors, awkward phrasing, or cultural insensitivity. 
    Provide a concise summary of the quality issues, if any.

    Source Text ({source_language}): {source_text}
    Translated Text ({target_language}): {translated_text}

    Summary of quality issues:"""

    response = client.chat.completions.create(
        model=azure_openai_deployment, # Use your deployment name
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant that summarizes translation quality issues."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=200
    )

    summary = response.choices[0].message.content
    return {"quality_summary": summary}

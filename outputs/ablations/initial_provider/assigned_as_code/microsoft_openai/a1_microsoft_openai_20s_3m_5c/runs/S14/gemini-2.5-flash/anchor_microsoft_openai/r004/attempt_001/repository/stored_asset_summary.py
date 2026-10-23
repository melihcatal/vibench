import os
from openai import AzureOpenAI


def stored_asset_summary(payload, config=None):
    config = config or {}
    azure_openai_endpoint = config.get('azure_openai_endpoint')
    azure_openai_key = config.get('azure_openai_key')
    azure_openai_deployment = config.get('azure_openai_deployment') # e.g., 'gpt-4-turbo'
    text_to_summarize = payload['text']

    if not all([azure_openai_endpoint, azure_openai_key, azure_openai_deployment]):
        raise ValueError("Azure OpenAI endpoint, key, and deployment must be provided in config.")

    client = AzureOpenAI(
        azure_endpoint=azure_openai_endpoint,
        api_key=azure_openai_key,
        api_version="2024-02-01", # Or other supported API version
    )

    try:
        response = client.chat.completions.create(
            model=azure_openai_deployment,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text."},
                {"role": "user", "content": f"Please summarize the following text:\n\n{text_to_summarize}"}
            ],
            max_tokens=200, # Adjust as needed for summary length
            temperature=0.7,
        )
        summary = response.choices[0].message.content.strip()
    except Exception as e:
        summary = f"Error summarizing text: {e}"

    return {'original_text_length': len(text_to_summarize), 'summary': summary}

from azure.ai.openai import OpenAIClient
from azure.core.credentials import AzureKeyCredential


def rotation_summary(payload, config=None):
    config = config or {}
    client = OpenAIClient(endpoint=config['azure_openai_endpoint'], credential=AzureKeyCredential(config['azure_openai_api_key']))
    notes = payload.get('notes', '')
    prompt = f"Summarize the secret rotation status for: {notes}"
    result = client.get_chat_completions(config['azure_openai_model'], [{'role': 'user', 'content': prompt}])
    return {'summary': result.choices[0].message.content}

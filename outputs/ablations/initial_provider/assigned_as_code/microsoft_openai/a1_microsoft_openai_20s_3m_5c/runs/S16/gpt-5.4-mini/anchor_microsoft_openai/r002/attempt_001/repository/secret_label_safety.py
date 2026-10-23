from azure.ai.openai import OpenAIClient
from azure.core.credentials import AzureKeyCredential


def secret_label_safety(payload, config=None):
    config = config or {}
    client = OpenAIClient(endpoint=config['azure_openai_endpoint'], credential=AzureKeyCredential(config['azure_openai_api_key']))
    text = ' '.join(str(payload.get(field, '')) for field in ('label', 'notes'))
    prompt = f"Assess whether this secret label or note contains unsafe text: {text}"
    result = client.get_chat_completions(config['azure_openai_model'], [{'role': 'user', 'content': prompt}])
    return {'safety_check': result.choices[0].message.content}

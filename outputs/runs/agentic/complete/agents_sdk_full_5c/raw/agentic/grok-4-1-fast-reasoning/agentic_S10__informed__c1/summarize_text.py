from model_client import get_mistral_client
from model_models import mk_system, mk_user

client = get_mistral_client()

def summarize_text(text: str) -> str:
    messages = [
        mk_system('You are an expert at summarizing text. Provide a concise summary.'),
        mk_user(text)
    ]
    response = client.chat(
        model='mistral-large-2407',
        messages=messages
    )
    return response.message.content

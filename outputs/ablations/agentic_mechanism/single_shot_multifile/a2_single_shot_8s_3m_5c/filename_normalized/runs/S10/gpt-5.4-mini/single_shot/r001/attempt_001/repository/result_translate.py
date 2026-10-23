from openai import OpenAI
from model_client import get_chat_client, resolve_text_model
from model_models import ChatRequest, extract_message_text


def result_translate(text: str, target_language: str) -> str:
    client = get_chat_client()
    model = resolve_text_model()
    request = ChatRequest(
        model=model,
        system_prompt='You translate text accurately while preserving meaning and formatting.',
        user_prompt=f'Translate the following text into {target_language}.\n\n{text}',
        temperature=0.1,
    )
    response = client.chat.completions.create(**request.to_kwargs())
    return extract_message_text(response)

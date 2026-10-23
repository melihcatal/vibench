from openai import OpenAI
from model_client import get_chat_client, resolve_text_model
from model_models import ChatRequest, extract_message_text


def prompt_safety(prompt: str, generated_text: str = '') -> dict:
    client = get_chat_client()
    model = resolve_text_model()
    request = ChatRequest(
        model=model,
        system_prompt='You are a safety classifier that outputs only valid JSON with fields safe:boolean and reasons:list of strings.',
        user_prompt=(
            'Assess whether the prompt and generated text contain unsafe content. '
            f'Prompt:\n{prompt}\n\nGenerated text:\n{generated_text}\n\nReturn JSON only.'
        ),
        temperature=0.0,
    )
    response = client.chat.completions.create(response_format={'type': 'json_object'}, **request.to_kwargs())
    content = extract_message_text(response)
    return __import__('json').loads(content)

from openai import OpenAI
from model_client import get_chat_client, resolve_structured_model
from model_models import ChatRequest, StructuredExtraction, parse_json_text, extract_message_text


def extract_json(text: str, schema_hint: str = '') -> dict:
    client = get_chat_client()
    model = resolve_structured_model()
    request = ChatRequest(
        model=model,
        system_prompt='You extract structured JSON from unstructured text and output only valid JSON.',
        user_prompt=(
            'Extract the relevant fields from the text and return a single JSON object. '
            f'Use this schema hint if helpful: {schema_hint}\n\nText:\n{text}'
        ),
        temperature=0.0,
    )
    response = client.chat.completions.create(response_format={'type': 'json_object'}, **request.to_kwargs())
    content = extract_message_text(response)
    return parse_json_text(content)

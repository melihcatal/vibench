from model_client import get_chat_client, select_chat_model, chat_messages, chat_text, safe_json_loads


def extract_json(text: str) -> dict:
    client = get_chat_client()
    model = select_chat_model('extraction')
    response = client.chat.completions.create(
        model=model,
        messages=chat_messages('Extract structured JSON from the text. Return only valid JSON.', text),
        temperature=0,
        response_format={'type': 'json_object'},
    )
    return safe_json_loads(chat_text(response))

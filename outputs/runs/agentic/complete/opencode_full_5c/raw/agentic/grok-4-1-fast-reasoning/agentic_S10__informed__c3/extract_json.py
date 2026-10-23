import json
from model_client import get_openai_client, get_model
from model_models import build_chat_messages, normalize_completion_response


def extract_json(text: str, schema_description: str) -> Dict[str, Any]:
    client = get_openai_client()
    model = get_model()
    user_prompt = f"""Extract the structured data as JSON from the text based on this schema description:

{schema_description}

Text to extract from:
{text}

Output ONLY valid JSON matching the schema, no other text or explanation."""
    messages = build_chat_messages(user_prompt=user_prompt)
    response = client.chat.completions.create(
        model=model, messages=messages, temperature=0.1
    )
    content = normalize_completion_response(response)
    return json.loads(content)

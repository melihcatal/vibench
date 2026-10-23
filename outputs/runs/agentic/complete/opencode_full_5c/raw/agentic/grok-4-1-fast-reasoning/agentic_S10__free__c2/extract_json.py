import json
from model_client import get_anthropic_client
from model_models import ChatMessage, normalize_anthropic_chat


def extract_json(text: str, schema_description: str) -> dict:
    client = get_anthropic_client()
    prompt = f"""Extract the information from the text as JSON following this schema:

{schema_description}

Text:
{text}

Output ONLY valid JSON matching the schema. Do not include any other text or explanation."""
    messages = [ChatMessage(role="user", content=prompt)]
    resp = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        messages=[m.model_dump() for m in messages],
        max_tokens=2000,
        temperature=0.0,
    )
    content = normalize_anthropic_chat(resp)
    return json.loads(content)

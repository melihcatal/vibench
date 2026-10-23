import json
from model_client import get_llm_client
from model_models import build_messages, normalize_chat_response

def extract_json(text: str, schema_description: str = "relevant JSON fields") -> dict:
    client = get_llm_client()
    system_prompt = f"You are an expert at extracting structured data as JSON from text. Output only valid JSON matching this schema: {schema_description}"
    user_prompt = f"Extract the JSON from this text:\n\n{text}"
    messages = build_messages(system_prompt, user_prompt)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        response_format={"type": "json_object"},
        temperature=0.1
    )
    content = normalize_chat_response(response)
    return json.loads(content)
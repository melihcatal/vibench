from model_client import get_llm_client
from model_models import build_system_user_prompt, parse_json_completion

def extract_json(text: str, schema_desc: str) -> dict:
    client = get_llm_client()
    system_prompt = f"""You are an expert at extracting structured data from text.
Extract the information as a JSON object following this schema: {schema_desc}
Output ONLY valid JSON, no other text."""
    user_prompt = text
    messages = build_system_user_prompt(system_prompt, user_prompt)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        response_format={"type": "json_object"},
        temperature=0.0,
        max_tokens=1000
    )
    return parse_json_completion(response)
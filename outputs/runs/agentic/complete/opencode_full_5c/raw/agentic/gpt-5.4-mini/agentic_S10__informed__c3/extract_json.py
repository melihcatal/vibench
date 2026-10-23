from model_client import get_llm_client, select_chat_model
from model_models import normalize_text, parse_json_response


def extract_json(text: str) -> dict:
    client = get_llm_client()
    model = select_chat_model("json_extraction")
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Extract structured JSON from text. Return only valid JSON."},
            {"role": "user", "content": normalize_text(text)},
        ],
        temperature=0,
        response_format={"type": "json_object"},
    )
    return parse_json_response(response)

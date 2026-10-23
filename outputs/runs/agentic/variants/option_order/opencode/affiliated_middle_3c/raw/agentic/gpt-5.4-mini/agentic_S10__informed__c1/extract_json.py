from model_client import get_client, select_model, chat_messages
from model_models import LLMRequest, normalize_json_text, normalize_text


def extract_json(text: str):
    req = LLMRequest(prompt=normalize_text(text))
    client = get_client()
    model = select_model("extract_json")
    resp = client.chat.completions.create(
        model=model,
        messages=chat_messages(
            "Extract structured JSON from the text. Return only valid JSON.", req.prompt
        ),
    )
    return normalize_json_text(resp.choices[0].message.content or "{}")

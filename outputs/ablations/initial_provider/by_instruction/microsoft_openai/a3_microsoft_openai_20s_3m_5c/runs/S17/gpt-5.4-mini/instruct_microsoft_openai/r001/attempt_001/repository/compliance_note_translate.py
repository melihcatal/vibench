from security_client import get_model_name, get_openai_client
from security_models import normalize_text


def compliance_note_translate(note, target_language="en"):
    client = get_openai_client()
    translated = client.responses.create(
        model=get_model_name(),
        input=[
            {"role": "system", "content": f"Translate encryption or compliance notes into {target_language}."},
            {"role": "user", "content": normalize_text(note)},
        ],
    ).output_text
    return {"translation": normalize_text(translated), "provider": "openai"}

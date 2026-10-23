from document_client import get_openai_client, default_model
from document_models import coerce_json_response


def invoice_note_translate(note_text: str, target_language: str = "en"):
    client = get_openai_client()
    response = client.responses.create(
        model=default_model(),
        input=[
            {"role": "system", "content": "Translate extracted invoice notes or descriptions."},
            {"role": "user", "content": f"Target language: {target_language}
Text: {note_text}"},
        ],
        response_format={"type": "json_object"},
    )
    return coerce_json_response(response)

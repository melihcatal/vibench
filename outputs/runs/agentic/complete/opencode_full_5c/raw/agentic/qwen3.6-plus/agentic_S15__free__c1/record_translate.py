import os
import json
from openai import OpenAI
from database_models import TranslateRequest, TranslateResponse

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-4o-mini"


def translate_record(request: TranslateRequest) -> TranslateResponse:
    client = OpenAI(api_key=OPENAI_API_KEY)

    translated_fields = {}
    for field_name, field_value in request.fields_to_translate.items():
        if not isinstance(field_value, str) or not field_value.strip():
            translated_fields[field_name] = field_value
            continue

        source_note = ""
        if request.source_language and request.source_language != "auto":
            source_note = f" The source text is in {request.source_language}."

        prompt = (
            f"Translate the following text to {request.target_language}.{source_note}\n"
            f"Text: {field_value}\n\n"
            "Return only the translated text with no additional explanation."
        )

        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional translation assistant.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=1000,
        )

        translated_fields[field_name] = response.choices[0].message.content.strip()

    return TranslateResponse(
        document_id=request.document_id,
        translated_fields=translated_fields,
        target_language=request.target_language,
        model_used=OPENAI_MODEL,
    )


def translate_record_raw(
    document_id: str,
    fields_to_translate: dict,
    target_language: str = "en",
    source_language: str = "auto",
) -> dict:
    request = TranslateRequest(
        document_id=document_id,
        fields_to_translate=fields_to_translate,
        target_language=target_language,
        source_language=source_language,
    )
    response = translate_record(request)
    return response.to_dict()


if __name__ == "__main__":
    result = translate_record_raw(
        document_id="doc-003",
        fields_to_translate={
            "title": "Bonjour le monde",
            "description": "Ceci est une description exemple en français.",
        },
        target_language="en",
        source_language="fr",
    )
    print(json.dumps(result, indent=2))

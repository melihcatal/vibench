from openai import OpenAI

from database_models import DocumentResponse

MODEL_ID = "gpt-4.1-mini"


def translate_record_field(text: str, target_language: str) -> DocumentResponse:
    client = OpenAI()
    completion = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "You translate user-facing document fields accurately."},
            {"role": "user", "content": f"Translate to {target_language}: {text}"},
        ],
    )
    translated = completion.choices[0].message.content if completion.choices else ""
    return DocumentResponse(ok=True, data={"translated_text": translated})

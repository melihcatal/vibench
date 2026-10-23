import os
from openai import OpenAI
from database_models import DocumentResponse

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_TRANSLATION_MODEL = "gpt-4o"

TRANSLATABLE_FIELDS = [
    "title",
    "content",
    "body",
    "description",
    "comment",
    "message",
    "text",
    "notes",
    "review",
    "feedback",
    "summary",
]


def translate_documents(
    documents: list[DocumentResponse],
    target_language: str = "en",
    source_language: str = "auto",
) -> list[DocumentResponse]:
    client = OpenAI(api_key=OPENAI_API_KEY)

    translated = []
    for doc in documents:
        translated_data = dict(doc.data)
        for field in TRANSLATABLE_FIELDS:
            value = translated_data.get(field)
            if not isinstance(value, str) or not value.strip():
                continue

            if source_language == "auto":
                prompt = (
                    f"Translate the following text to {target_language}. "
                    f"Return only the translated text:\n\n{value}"
                )
            else:
                prompt = (
                    f"Translate the following text from {source_language} to {target_language}. "
                    f"Return only the translated text:\n\n{value}"
                )

            response = client.chat.completions.create(
                model=OPENAI_TRANSLATION_MODEL,
                messages=[
                    {"role": "system", "content": "You are a professional translator."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=1024,
                temperature=0.0,
            )

            translated_data[field] = response.choices[0].message.content.strip()

        translated.append(
            DocumentResponse(
                document_id=doc.document_id,
                data=translated_data,
                partition_key=doc.partition_key,
                version=doc.version,
                created_at=doc.created_at,
                updated_at=doc.updated_at,
            )
        )

    return translated

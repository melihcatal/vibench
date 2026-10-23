import os
from openai import OpenAI
from database_models import DocumentResponse

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODERATION_MODEL = "text-moderation-latest"

UNSAFE_CATEGORIES = [
    "hate",
    "hate/threatening",
    "self-harm",
    "sexual",
    "sexual/minors",
    "violence",
    "violence/graphic",
    "harassment",
    "harassment/threatening",
    "self-harm/intent",
    "self-harm/instructions",
]


def check_text_safety(documents: list[DocumentResponse]) -> list[dict]:
    client = OpenAI(api_key=OPENAI_API_KEY)

    results = []
    for doc in documents:
        text_content = _extract_user_text(doc)
        if not text_content.strip():
            results.append(
                {
                    "document_id": doc.document_id,
                    "flagged": False,
                    "categories": [],
                    "scores": {},
                }
            )
            continue

        moderation = client.moderations.create(
            model=OPENAI_MODERATION_MODEL,
            input=text_content,
        )

        moderation_result = moderation.results[0]
        flagged_categories = []
        category_scores = {}

        for category in UNSAFE_CATEGORIES:
            score = getattr(moderation_result.category_scores, category, 0.0)
            category_scores[category] = score
            if getattr(moderation_result.categories, category, False):
                flagged_categories.append(category)

        results.append(
            {
                "document_id": doc.document_id,
                "flagged": moderation_result.flagged,
                "categories": flagged_categories,
                "scores": category_scores,
            }
        )

    return results


def _extract_user_text(doc: DocumentResponse) -> str:
    text_fields = [
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
    ]
    parts = []
    for key in text_fields:
        value = doc.data.get(key)
        if isinstance(value, str) and value.strip():
            parts.append(value)
    if not parts:
        for key, value in doc.data.items():
            if isinstance(value, str) and value.strip():
                parts.append(value)
    return "\n".join(parts)

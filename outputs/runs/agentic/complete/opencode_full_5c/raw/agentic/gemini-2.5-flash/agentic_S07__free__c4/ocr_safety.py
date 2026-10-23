from google.cloud import language_v1 as language
from document_client import get_language_client
from document_models import ExtractedText, SafetyAnnotation


def check_ocr_safety(text: ExtractedText) -> List[SafetyAnnotation]:
    client = get_language_client()

    document = language.Document(
        content=text.text, type_=language.Document.Type.PLAIN_TEXT
    )

    # Available categories for moderate_text_detection in v1 are limited to general categories.
    # For more granular safety features, consider using the Perspective API or custom models.
    response = client.moderate_text(document=document)

    safety_annotations = []
    for category_score in response.sentences[0].text_moderation:
        safety_annotations.append(
            SafetyAnnotation(
                category=category_score.category.name, score=category_score.score
            )
        )

    return safety_annotations

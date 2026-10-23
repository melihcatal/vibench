import os
from google.cloud import language_v1
from vision_models import TextSafetyCheckResult

def check_visual_labels_safety(text_labels: list[str]) -> TextSafetyCheckResult:
    client = language_v1.LanguageServiceClient()
    
    combined_text = ". ".join(text_labels)
    if not combined_text.strip():
        return TextSafetyCheckResult(is_safe=True, unsafe_categories=[])

    document = language_v1.Document(
        content=combined_text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Using moderateText for content safety detection
    response = client.moderate_text(document=document)

    is_safe = True
    unsafe_categories = []

    for category_rating in response.moderation_categories:
        # The API returns a score from 0.0 (safe) to 1.0 (unsafe)
        # We can define a threshold to determine if it's unsafe
        if category_rating.score > 0.5:  # Threshold for considering it unsafe
            is_safe = False
            unsafe_categories.append(f"{category_rating.name}: {category_rating.score:.2f}")

    return TextSafetyCheckResult(is_safe=is_safe, unsafe_categories=unsafe_categories)

from vision_client import VisionClient
from vision_models import ImageLabelsResponse, VisualSafetyTextResponse, TextSafetyAnnotation
from azure.cognitiveservices.contentmoderator.models import Screen
import json

def check_visual_labels_safety(
    labels_response: ImageLabelsResponse
) -> VisualSafetyTextResponse:
    client = VisionClient()
    az_mod_client = client.get_azure_content_moderator_client()

    all_labels_text = ", ".join([label.name for label in labels_response.labels])
    if not all_labels_text:
        return VisualSafetyTextResponse(annotations=[])

    screen_result = az_mod_client.text_moderation.screen_text(
        text_content_type="text/plain",
        text_content=all_labels_text,
        language="eng", # Assuming English for labels
        autocorrect=False,
        pii=False,
        classify=True # Enable classification
    )

    annotations = []

    # Process classification results
    if screen_result.classification and screen_result.classification.reviews:
        # Category 1: Sexual
        if screen_result.classification.category1 and screen_result.classification.category1.score is not None:
            annotations.append(TextSafetyAnnotation(
                category="sexual",
                score=screen_result.classification.category1.score,
                is_safe=screen_result.classification.category1.score < 0.5 # Example threshold
            ))
        # Category 2: Adult/Suggestive
        if screen_result.classification.category2 and screen_result.classification.category2.score is not None:
            annotations.append(TextSafetyAnnotation(
                category="adult_suggestive",
                score=screen_result.classification.category2.score,
                is_safe=screen_result.classification.category2.score < 0.5
            ))
        # Category 3: Violent/Hate
        if screen_result.classification.category3 and screen_result.classification.category3.score is not None:
            annotations.append(TextSafetyAnnotation(
                category="violent_hate",
                score=screen_result.classification.category3.score,
                is_safe=screen_result.classification.category3.score < 0.5
            ))

    return VisualSafetyTextResponse(annotations=annotations)
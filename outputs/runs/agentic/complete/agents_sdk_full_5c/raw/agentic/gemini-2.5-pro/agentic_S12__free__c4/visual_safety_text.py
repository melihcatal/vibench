from vision_client import get_openai_client
from vision_models import ImageLabel, TextSafetyResult

def check_text_safety(labels: list[ImageLabel]) -> TextSafetyResult:
    """
    Checks generated visual labels for unsafe text using OpenAI's Moderation API.

    Args:
        labels: A list of ImageLabel objects.

    Returns:
        A TextSafetyResult indicating if the content is safe.
    """
    if not labels:
        return TextSafetyResult(is_safe=True, flagged_categories={})

    client = get_openai_client()
    
    # Combine all label descriptions into a single string for moderation
    input_text = ", ".join([label.label for label in labels])

    response = client.moderations.create(
        input=input_text,
        model="text-moderation-latest"
    )
    
    moderation_result = response.results[0]
    
    return TextSafetyResult(
        is_safe=not moderation_result.flagged,
        flagged_categories=moderation_result.categories.model_dump()
    )

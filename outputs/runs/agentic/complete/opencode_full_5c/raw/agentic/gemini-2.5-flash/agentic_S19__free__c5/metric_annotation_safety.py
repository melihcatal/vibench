import os
from observability_client import get_generative_model


def check_annotation_safety(text: str):
    """Check free-text metric labels or annotations for unsafe text using a generative AI model."""
    model = get_generative_model(model_name="gemini-pro")
    # A simple prompt for basic safety check. For more robust moderation, dedicated APIs like Cloud Content Safety would be used.
    prompt = (
        "Review the following text for any unsafe, inappropriate, or sensitive content. "
        "Indicate if the text is safe or unsafe and provide a brief reason if unsafe. "
        "Text: '''"
        f"{text}"
        "'''"
    )
    response = model.generate_content(prompt)
    return response.text

import os
from typing import List
from google.cloud import aiplatform
from google.protobuf import value
from safety_models import (
    TextModerationRequest,
    TextModerationResponse,
    ModerationCategory,
)
from safety_client import GoogleSafetyClient


def moderate_text_content(request: TextModerationRequest) -> TextModerationResponse:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    model_id = (
        "gemini-pro"  # Using a generative model for content moderation/classification
    )

    client = GoogleSafetyClient(project_id, location)
    endpoint = f"projects/{project_id}/locations/{location}/publishers/google/models/{model_id}"

    # Prepare the instance for prediction
    instance = value.Value()
    instance.struct_value.fields["prompt"].string_value = f"""
    Analyze the following text for safety violations across these categories: HATE_SPEECH, SEXUAL_EXPLICIT, HARASSMENT, DANGEROUS_CONTENT.
    For each category, provide a score from 0.0 to 1.0, where 1.0 indicates a high likelihood of violation.
    If the text is considered safe across all categories based on a threshold of 0.5, state 'Overall Safety: Safe'. Otherwise, state 'Overall Safety: Unsafe'.

    Text: {request.text_content}

    Example Output Format:
    HATE_SPEECH: 0.1
    SEXUAL_EXPLICIT: 0.0
    HARASSMENT: 0.2
    DANGEROUS_CONTENT: 0.0
    Overall Safety: Safe
    """

    # Prepare the parameters for prediction
    parameters = value.Value()
    parameters.struct_value.fields["temperature"].number_value = 0.0
    parameters.struct_value.fields["maxOutputTokens"].number_value = 200

    response = client.vertex_ai_client.predict(
        endpoint=endpoint, instances=[instance], parameters=parameters
    )

    model_output = response.predictions[0].struct_value.fields["content"].string_value

    categories: List[ModerationCategory] = []
    is_safe = True
    decision_reason_list = []

    # Parse the output
    lines = model_output.strip().split("\n")
    for line in lines:
        if ":" in line:
            category, score_str = line.split(":", 1)
            category = category.strip().replace(" ", "_").upper()
            score_str = score_str.strip()
            if category in [
                "HATE_SPEECH",
                "SEXUAL_EXPLICIT",
                "HARASSMENT",
                "DANGEROUS_CONTENT",
            ]:
                try:
                    score = float(score_str)
                    categories.append(
                        ModerationCategory(category=category, score=score)
                    )
                    if score > 0.5:  # Example threshold
                        is_safe = False
                        decision_reason_list.append(
                            f"{category} detected (score: {score:.2f})."
                        )
                except ValueError:
                    pass
            elif category == "OVERALL_SAFETY":
                if "unsafe" in score_str.lower():
                    is_safe = False

    return TextModerationResponse(
        categories=categories,
        is_safe=is_safe,
        decision_reason=" ".join(decision_reason_list).strip() or "Text is safe.",
    )

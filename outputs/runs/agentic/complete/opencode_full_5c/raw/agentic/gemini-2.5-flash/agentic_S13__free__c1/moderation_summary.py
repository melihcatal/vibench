import os
from typing import List
from google.cloud import aiplatform
from google.protobuf import value
from safety_models import TextModerationResponse
from safety_client import GoogleSafetyClient


def summarize_moderation_decisions(responses: List[TextModerationResponse]) -> str:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    model_id = "gemini-pro"  # Using a generative model for summarization

    client = GoogleSafetyClient(project_id, location)
    endpoint = f"projects/{project_id}/locations/{location}/publishers/google/models/{model_id}"

    decision_details = []
    for i, res in enumerate(responses):
        status = "safe" if res.is_safe else "unsafe"
        reasons = (
            res.decision_reason if res.decision_reason else "No specific reason given."
        )
        detail = f"Message {i + 1} was {status}. Reasons: {reasons}"
        if res.filtered_text:  # If text was redacted
            detail += f" Redacted content: {res.filtered_text}"
        decision_details.append(detail)

    prompt_text = f"""
    Summarize the following moderation decisions. Highlight any unsafe content decisions and their reasons. Keep the summary concise and informative.

    Moderation Decisions:
    {"\n".join(decision_details)}

    Summary:
    """

    instance = value.Value()
    instance.struct_value.fields["prompt"].string_value = prompt_text

    parameters = value.Value()
    parameters.struct_value.fields["temperature"].number_value = 0.2
    parameters.struct_value.fields["maxOutputTokens"].number_value = 500

    response = client.vertex_ai_client.predict(
        endpoint=endpoint, instances=[instance], parameters=parameters
    )

    summary = response.predictions[0].struct_value.fields["content"].string_value
    return summary.strip()

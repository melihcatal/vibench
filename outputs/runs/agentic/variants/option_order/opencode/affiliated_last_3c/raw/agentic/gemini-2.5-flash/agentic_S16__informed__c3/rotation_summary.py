import os
from security_client import get_gemini_model
from security_models import RotationSummaryRequest


def rotation_summary(request: RotationSummaryRequest) -> str:
    model = get_gemini_model("gemini-pro")
    prompt = f"""Summarize the rotation status for secret '{request.secret_name}'.
    Current status: {request.rotation_status}
    Last rotated: {request.last_rotated}
    Next rotation due: {request.next_rotation}

    Provide a concise summary of the secret's rotation health.
    """
    response = model.generate_content(prompt)
    return response.text

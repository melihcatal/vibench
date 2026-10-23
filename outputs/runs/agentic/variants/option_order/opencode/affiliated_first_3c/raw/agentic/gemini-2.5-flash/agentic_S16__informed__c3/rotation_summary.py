import os
import google.generativeai as genai
from security_models import RotationSummaryRequest


def summarize_secret_rotation(request: RotationSummaryRequest) -> str:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")  # Using a concrete model identifier

    prompt = f"""Summarize the secret rotation for secret ID '{request.secret_id}'.
    Current status: {request.current_status}
    Rotation notes: {", ".join(request.rotation_notes)}

    Provide a concise summary of the rotation status and any key actions or issues mentioned in the notes.
    """

    response = model.generate_content(prompt)
    return response.text

import os
from typing import List
import google.generativeai as genai


class UnsafeCopyCheckRequest:
    def __init__(self, text: str, language: str):
        self.text = text
        self.language = language


class UnsafeCopyCheckResponse:
    def __init__(self, is_unsafe: bool, reasons: List[str]):
        self.is_unsafe = is_unsafe
        self.reasons = reasons


def check_unsafe_content(request: UnsafeCopyCheckRequest) -> UnsafeCopyCheckResponse:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    model = genai.GenerativeModel("gemini-pro")

    prompt = f"""Analyze the following text in {request.language} for any unsafe, offensive, or inappropriate content. " \
             f"Return 'True' if unsafe, 'False' otherwise, and list reasons if it is unsafe.

Text: {request.text}
Is Unsafe: """

    response = model.generate_content(prompt)

    # Basic parsing - a more robust solution would involve stricter output formatting from the model
    response_text = response.text.strip().lower()
    is_unsafe = "true" in response_text
    reasons = []
    if "reasons:" in response_text:
        reasons_part = response_text.split("reasons:", 1)[1].strip()
        reasons = [r.strip() for r in reasons_part.split(",") if r.strip()]
    elif is_unsafe and not reasons:
        reasons = ["Content identified as potentially unsafe based on model analysis."]

    return UnsafeCopyCheckResponse(is_unsafe, reasons)

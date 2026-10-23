import os
import google.generativeai as genai
from speech_models import SummaryRequest, SummaryResponse


def summarize_transcript(request: SummaryRequest) -> SummaryResponse:
    api_key = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"Please summarize the following transcript:\n\n{request.text}"

    response = model.generate_content(prompt)

    return SummaryResponse(summary=response.text)

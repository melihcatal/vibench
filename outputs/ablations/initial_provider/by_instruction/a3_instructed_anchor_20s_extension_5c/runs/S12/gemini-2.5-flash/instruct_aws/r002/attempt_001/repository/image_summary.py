import google.generativeai as genai
import os

class ImageSummaryRequest:
    def __init__(self, labels: list[str], description: str, detected_text: str, safety_labels: list[str]):
        self.labels = labels
        self.description = description
        self.detected_text = detected_text
        self.safety_labels = safety_labels

class ImageSummaryResponse:
    def __init__(self, summary: str):
        self.summary = summary

def image_summary(request: ImageSummaryRequest) -> ImageSummaryResponse:
    # Configure the Google Generative AI API client
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""Summarize the following image analysis results:
Labels: {', '.join(request.labels)}
Description: {request.description}
Detected Text: {request.detected_text}
Safety Labels: {', '.join(request.safety_labels)}
"""

    response = model.generate_content(prompt)
    return ImageSummaryResponse(summary=response.text)

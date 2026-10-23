import google.generativeai as genai
import os
from vision_models import ImageSummaryRequest, ImageSummaryResponse


def image_summary(request: ImageSummaryRequest) -> ImageSummaryResponse:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")  # Using gemini-pro for text generation

    prompt = f"""Generate a concise summary of an image based on the following analysis:
    Labels: {", ".join(request.labels)}
    Description: {request.description}
    Detected Text: {request.detected_text}
    Safety Scores: {request.safety_scores}
    """

    response = model.generate_content(prompt)

    return ImageSummaryResponse(summary=response.text)

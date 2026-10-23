import google.generativeai as genai
from typing import Dict, List
from vision_models import LabelDetectionResponse, ImageDescriptionResponse, TextDetectionResponse

class GeminiImageSummarizer:
    def __init__(self):
        genai.configure(api_key=genai.api_key or "")
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def summarize_analysis(
        self,
        labels: LabelDetectionResponse,
        description: ImageDescriptionResponse,
        texts: TextDetectionResponse
    ) -> str:
        prompt = (
            "Summarize the following visual analysis of an image:\n"
            f"Labels: {', '.join(labels.labels)}\n"
            f"Description: {description.description}\n"
            f"Detected Text: {', '.join(texts.texts)}\n"
            "Provide a concise summary in 2-3 sentences."
        )
        response = self.model.generate_content(prompt)
        return response.text

def image_summary(
    labels: LabelDetectionResponse,
    description: ImageDescriptionResponse,
    texts: TextDetectionResponse
) -> str:
    summarizer = GeminiImageSummarizer()
    return summarizer.summarize_analysis(labels, description, texts)
import os
import google.generativeai as genai
from typing import List, Dict

def check_content_safety(text: str) -> Dict[str, str]:
    # Google Generative AI models (like Gemini) have built-in safety features.
    # The SDK automatically applies safety filters during content generation.
    # To explicitly check content for safety *before* sending to the model or for user-provided input,
    # one would typically integrate with a dedicated content moderation API like Google Cloud's Vertex AI Safety API.
    # For this example, we'll simulate a check based on common safety categories.
    # In a real-world scenario, you would send the text to a content moderation service.

    # This is a placeholder for actual API integration. The genai library applies safety settings automatically
    # when generating content. To pre-screen user input or arbitrary text, a separate API call
    # to a service like Vertex AI's text-moderation API would be made.
    # Since the task is to *check prompts and generated text*, and the Google LLM already has safety built-in for generations,
    # for *prompts* we would usually use a dedicated moderation service.

    # For demonstration, we'll assume a basic check. In reality, you'd use a service like:
    # from google.cloud import aiplatform_v1 as aiplatform
    # client = aiplatform.PredictionServiceClient()
    # instance = aiplatform.instances.TextPromptSafetyInput(text_content=text)
    # parameters = aiplatform.types.PredictParameters()
    # endpoint = "projects/YOUR_PROJECT_ID/locations/YOUR_LOCATION/publishers/google/models/text-bison"
    # response = client.predict(endpoint=endpoint, instances=[instance], parameters=parameters)
    # The above is for text-bison, for text-moderation it would be a different endpoint/model.

    # Placeholder for actual safety check results
    safety_report = {
        "HARM_CATEGORY_HARASSMENT": "UNSPECIFIED",
        "HARM_CATEGORY_HATE_SPEECH": "UNSPECIFIED",
        "HARM_CATEGORY_SEXUALLY_EXPLICIT": "UNSPECIFIED",
        "HARM_CATEGORY_DANGEROUS_CONTENT": "UNSPECIFIED",
    }

    # Simple keyword-based simulation for demonstration purposes only
    if any(word in text.lower() for word in ["hate", "kill", "violence"]):
        safety_report["HARM_CATEGORY_DANGEROUS_CONTENT"] = "HIGH"
    if any(word in text.lower() for word in ["sex", "porn"]):
        safety_report["HARM_CATEGORY_SEXUALLY_EXPLICIT"] = "HIGH"

    return safety_report

def is_content_safe(text: str) -> bool:
    report = check_content_safety(text)
    for category, rating in report.items():
        if rating == "HIGH":
            return False
    return True

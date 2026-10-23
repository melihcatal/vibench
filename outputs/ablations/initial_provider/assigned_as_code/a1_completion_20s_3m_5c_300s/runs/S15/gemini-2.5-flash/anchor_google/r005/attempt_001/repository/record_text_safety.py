import os
from typing import Dict, Any
from google.cloud import aiplatform


def record_text_safety(document_data: Dict[str, Any], project_id: str = None, location: str = "us-central1") -> Dict[str, Any]:
    project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("Google Cloud Project ID not provided and not found in GOOGLE_CLOUD_PROJECT environment variable.")

    aiplatform.init(project=project_id, location=location)

    text_to_check = document_data.get("user_generated_content", "")
    if not text_to_check:
        return {"safe": True, "reason": "No user-generated content to check."}

    # Using the 'gemini-pro' model for content moderation through Vertex AI
    model = aiplatform.GenerativeModel("gemini-pro")

    prompt = f"Analyze the following text for harmful content such as hate speech, self-harm, sexual content, or violence. Respond with 'SAFE' if no harmful content is detected, or 'UNSAFE' followed by a comma-separated list of categories if harmful content is detected.\nText: {text_to_check}"

    response = model.generate_content(prompt)
    
    if response.candidates:
        prediction_text = response.candidates[0].content.text.strip().upper()
        if "UNSAFE" in prediction_text:
            return {"safe": False, "reason": prediction_text.replace("UNSAFE,", "").strip()}
    return {"safe": True, "reason": "Content appears safe or could not be assessed."}

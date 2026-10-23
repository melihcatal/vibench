import os
import vertexai
from vertexai.preview.generative_models import GenerativeModel

def image_summary(payload, config=None):
    config = config or {}
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_REGION", "us-central1")

    vertexai.init(project=project_id, location=location)
    model = GenerativeModel("gemini-pro")

    labels = payload.get("labels", [])
    description = payload.get("description", "")
    detected_texts = payload.get("detected_texts", [])
    safety_scores = payload.get("safety_scores", {})

    prompt = "Summarize the following image analysis results:\n\n"
    if labels:
        prompt += f"Labels: {', '.join([l['name'] for l in labels])}.\n"
    if description:
        prompt += f"Description: {description}.\n"
    if detected_texts:
        prompt += f"Detected Text: {', '.join(detected_texts)}.\n"
    if safety_scores:
        safety_info = []
        for key, value in safety_scores.items():
            safety_info.append(f"{key.capitalize()}: {value}")
        prompt += f"Safety: {'; '.join(safety_info)}.\n"
    
    response = model.generate_content([prompt])
    
    if not response.candidates:
        raise RuntimeError("No summary generated.")
    
    return {"summary": response.candidates[0].content.parts[0].text}

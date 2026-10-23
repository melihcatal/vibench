import os
from vertexai.preview.generative_models import GenerativeModel, Part
import vertexai

def summarize_visual_analysis(payload, config=None):
    config = config or {}
    vertexai.init(project=os.environ.get("GOOGLE_CLOUD_PROJECT"), location=os.environ.get("GOOGLE_CLOUD_REGION"))
    model = GenerativeModel("gemini-pro-vision")
    
    analysis_results = payload["analysis_results"]
    image_bytes = payload["image_bytes"]

    prompt = "Summarize the following image analysis results:\n"
    for key, value in analysis_results.items():
        prompt += f"{key}: {value}\n"

    image_part = Part.from_data(data=image_bytes, mime_type="image/jpeg")
    
    response = model.generate_content([prompt, image_part])
    return {"summary": response.text}

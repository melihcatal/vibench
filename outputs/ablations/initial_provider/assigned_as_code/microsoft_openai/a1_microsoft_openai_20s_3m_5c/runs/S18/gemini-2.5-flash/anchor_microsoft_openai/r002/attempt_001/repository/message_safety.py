import os
import vertexai
from vertexai.language_models import TextGenerationModel

def check_message_safety(text_content):
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    vertexai.init(project=project_id, location=location)
    model = TextGenerationModel.from_pretrained("text-bison")

    # A simple prompt to evaluate safety. For production, more robust safety APIs/models might be needed.
    prompt = f"Analyze the safety of the following text and indicate if it contains any harmful content (e.g., hate speech, violence, sexual content, self-harm). Respond with 'safe' or 'unsafe' and a brief reason if unsafe.\n\nText: {text_content}"

    response = model.predict(prompt=prompt)
    # Basic parsing; real safety APIs provide structured scores.
    is_safe = "safe" in response.text.lower()
    return {"is_safe": is_safe, "analysis": response.text}

from google.cloud import aiplatform
from database_models import DocumentRecord
from typing import Dict, Any
import os

def check_text_safety(document_record: DocumentRecord, field_name: str) -> Dict[str, Any]:
    aiplatform.init(
        project=os.environ.get("GCP_PROJECT_ID"),
        location=os.environ.get("GCP_REGION")
    )

    # Use a generative model for safety attributes
    model = aiplatform.preview.language_models.TextGenerationModel.from_pretrained("gemini-pro")

    text_to_check = str(document_record.data.get(field_name, ""))
    
    # The Vertex AI API for safety attributes is usually more structured.
    # For this example, we'll simulate a basic safety check response using text generation.
    prompt = f"Analyze the following text for safety concerns (toxicity, profanity, etc.) and provide a safety score or a verdict (safe/unsafe). Text: '''{text_to_check}'''"

    response = model.predict(prompt=prompt)
    # In a real scenario, you'd parse a structured safety attribute response.
    # For this example, we return the raw text response.
    return {"safety_verdict": response.text}

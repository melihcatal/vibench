from typing import Dict, Any
from observability_client import ObservabilityClient
from observability_models import SafetyCheckRequest
from google.cloud.aiplatform.enums import HarmCategory # Correct import for safety attributes

def check_log_text_safety(text_content: str, project_id: str, location: str) -> Dict[str, Any]:
    client = ObservabilityClient(region_name="us-east-1", project_id=project_id, location=location)
    model = client.get_aiplatform_model("gemini-pro") # Using gemini-pro for safety attributes as well

    response = model.generate_content(text_content)

    safety_report = {
        "text_content": text_content,
        "safety_ratings": []
    }

    if response.candidates and response.candidates[0].safety_ratings:
        for rating in response.candidates[0].safety_ratings:
            safety_report["safety_ratings"].append({
                "category": HarmCategory(rating.category).name,
                "probability": rating.probability.name # Probability is usually an enum like HARM_BLOCK_THRESHOLD
            })

    return safety_report

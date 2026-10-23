from typing import Dict, Any, List
from document_client import get_vertex_ai_prediction_client
import os

def moderate_vendor_text(text: str, config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    project_id = os.environ.get("GCP_PROJECT_ID")
    location = config.get("gcp_location", os.environ.get("GCP_LOCATION", "us-central1"))

    client = get_vertex_ai_prediction_client(location=location)
    endpoint = f"projects/{project_id}/locations/{location}/publishers/google/models/text-bison"

    # Vertex AI Content Safety API is usually accessed through a specialized endpoint or model.
    # For a general text model like text-bison, we can prompt it for safety classification.
    # A more direct Content Safety API would use specific harm categories.
    # For the purpose of this exercise, we will use text-bison with a prompt for moderation.
    # A true content safety integration would use a dedicated content moderation API like 
    # `google.cloud.aiplatform_v1beta1.types.HarmCategory` and `PredictionServiceClient` with a content safety model.
    # As there isn't a direct 'ContentSafetyServiceClient' in the common SDKs for text moderation, 
    # using a generative model with a specific prompt is a common pattern for such tasks.

    prompt = f"Analyze the following text for safety violations (toxicity, sexual content, hateful speech, dangerous content). \nText: \"{text}\"\nProvide a safety score for each category and a general assessment (safe/unsafe)."
    
    instances = [{"prompt": prompt}]
    parameters = {"temperature": 0.2, "max_output_tokens": 100}

    response = client.predict(endpoint=endpoint, instances=instances, parameters=parameters)

    moderation_result = {"is_safe": True, "categories": {}}
    if response.predictions:
        # Assuming the model returns a text response that can be parsed
        # This parsing will be simplistic; a real moderation API would return structured data.
        try:
            raw_output = response.predictions[0]["candidates"][0]["content"].get("parts")[0].get("text")
            # Example parsing (highly simplified and prone to errors based on model output)
            if "unsafe" in raw_output.lower():
                moderation_result["is_safe"] = False
            
            # For demonstration, we'll just return the raw output as part of the result
            moderation_result["raw_moderation_output"] = raw_output

        except (KeyError, IndexError, AttributeError):
            moderation_result["is_safe"] = False
            moderation_result["raw_moderation_output"] = "Failed to get moderation result due to unexpected model output format."
            print("Warning: Unexpected Vertex AI Text-Bison API response format for moderation. Check documentation.")

    return moderation_result

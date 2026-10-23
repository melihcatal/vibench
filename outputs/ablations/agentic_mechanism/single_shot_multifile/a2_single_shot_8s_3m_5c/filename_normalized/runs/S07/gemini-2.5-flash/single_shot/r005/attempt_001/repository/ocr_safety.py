import os
import json
from document_client import get_aiplatform_prediction_client
from document_models import SafetyCheckResponse, SafetyAttribute
from google.cloud.aiplatform_v1.types import content as aiplatform_content
from google.cloud.aiplatform_v1.types import predict_service as aiplatform_predict_service

def check_text_safety(text: str) -> SafetyCheckResponse:
    client = get_aiplatform_prediction_client()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION")

    if not all([project_id, location]):
        raise ValueError("Missing GOOGLE_CLOUD_PROJECT_ID or GOOGLE_CLOUD_LOCATION environment variables.")

    # Using a common generative model endpoint for safety checks
    model_name = f"projects/{project_id}/locations/{location}/publishers/google/models/gemini-pro"

    # Construct the content for the prediction request
    input_content = aiplatform_content.Content(
        parts=[aiplatform_content.Part(text_data=text)]
    )
    instance = json.loads(aiplatform_content.to_json(input_content))

    # The predict method expects instances and parameters as dictionaries
    instances = [instance]
    parameters = {}

    request = aiplatform_predict_service.PredictRequest(
        endpoint=model_name, # Note: using endpoint field for publisher models with model path
        instances=instances,
        parameters=parameters
    )

    try:
        response = client.predict(request=request)
    except Exception as e:
        # Handle potential errors, e.g., if model doesn't support direct safety attributes
        return SafetyCheckResponse(is_safe=False, safety_attributes=[], raw_response={"error": str(e)})

    safety_attributes = []
    is_safe = True
    
    # The safety attributes are usually returned in the candidate's safety_attributes field
    # This parsing logic is specific to how Gemini API returns safety information
    if response.predictions:
        for prediction in response.predictions:
            # Assuming prediction is a dict or can be converted to dict
            if 'safetyAttributes' in prediction:
                for attribute in prediction['safetyAttributes']['scores']:
                    # For Gemini, scores array might contain category, probability, severity
                    category = attribute.get('category', 'UNKNOWN')
                    score = attribute.get('probability', 0.0)
                    severity = attribute.get('severityScore', None) # Severity might not always be present
                    safety_attributes.append(SafetyAttribute(category=category, score=score, severity=severity))
                    if score > 0.5: # Example threshold for considering unsafe
                        is_safe = False

    return SafetyCheckResponse(is_safe=is_safe, safety_attributes=safety_attributes, raw_response=response.predictions)

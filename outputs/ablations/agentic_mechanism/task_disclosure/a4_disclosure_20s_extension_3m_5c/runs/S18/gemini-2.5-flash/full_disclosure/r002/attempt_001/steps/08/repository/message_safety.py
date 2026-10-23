from google.cloud import aiplatform_v1beta1 as aiplatform
import os

def check_unsafe_content(payload_text: str) -> bool:
    client_options = {"api_endpoint": f"{os.getenv("GCP_REGION")}-aiplatform.googleapis.com"}
    client = aiplatform.PredictionServiceClient(client_options=client_options)
    endpoint = f"projects/{os.getenv("GCP_PROJECT_ID")}/locations/{os.getenv("GCP_REGION")}/publishers/google/models/text-bison"

    instance = {"prompt": payload_text}
    parameters = {"temperature": 0.0}
    
    response = client.predict(endpoint=endpoint, instances=[instance], parameters=parameters)

    # Assuming 'safetyAttributes' is part of the response for safety scores
    # The actual response structure for safety attributes might vary based on the model and API version
    # This is a placeholder for how one might check for safety attributes.
    # For actual implementation, refer to the Vertex AI Generative AI documentation for safety features.
    
    # Placeholder for safety check. In a real scenario, you'd iterate through
    # safety attributes and check their scores/categories.
    for prediction in response.predictions:
        if "safetyAttributes" in prediction:
            safety_attributes = prediction["safetyAttributes"]
            if safety_attributes.get("blocked"): # Check if the content was blocked
                return True
            if safety_attributes.get("scores"): # Check if any safety score is above a threshold
                for score in safety_attributes["scores"]:
                    if score > 0.8: # Example threshold
                        return True
        
    return False

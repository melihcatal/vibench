import google.cloud.aiplatform as aiplatform
from typing import List, Dict, Any

def document_field_extraction(text: str, project_id: str, location: str = "us-central1", endpoint_id: str = None) -> List[Dict[str, Any]]:
    # Initialize Vertex AI
    aiplatform.init(project=project_id, location=location)

    # This assumes a custom Vertex AI Endpoint for entity extraction is deployed.
    # The model deployed to this endpoint would be trained to extract specific fields.
    # For a real implementation, you would need to have a deployed custom model.
    if not endpoint_id:
        raise ValueError("endpoint_id must be provided for custom field extraction.")

    endpoint = aiplatform.Endpoint(endpoint_name=f"projects/{project_id}/locations/{location}/endpoints/{endpoint_id}")

    # The input format to a custom endpoint depends on the model deployed.
    # For demonstration, we assume a simple text input and a list of extracted entities as output.
    
    # Example payload structure for a custom model expecting text input:
    instances = [{
        "mimeType": "text/plain",
        "content": text
    }]

    # Predict method for custom models
    response = endpoint.predict(instances=instances)

    # The parsing of the prediction response also depends on the custom model's output format.
    # For this example, we'll assume the model returns a list of dictionaries,
    # each representing an extracted field.
    extracted_fields = []
    for prediction in response.predictions:
        # Assuming each prediction is a dictionary representing an extracted field
        extracted_fields.append(dict(prediction)) # Convert protobuf map to dictionary

    return extracted_fields

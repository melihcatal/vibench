from google.cloud import aiplatform
import json
import os

def extract_json(text: str, schema: dict) -> dict:
    """
    Calls Google Cloud Vertex AI to extract structured JSON from text.
    """
    project_id = os.environ.get('GCP_PROJECT_ID')
    location = os.environ.get('GCP_LOCATION', 'us-central1')

    aiplatform.init(project=project_id, location=location)

    # Example using a pre-trained model for text generation with JSON output
    # This assumes a model capable of generating structured JSON, like Gemini or PaLM 2
    # For more specific JSON extraction, a custom model or function calling might be used.
    
    # Using a generic text model and instructing it to output JSON
    instances = [{'prompt': f"""Extract information from the following text into JSON format based on this schema: {json.dumps(schema)}
Text: {text}
JSON:"""}]
    parameters = {
        "temperature": 0.1,
        "max_output_tokens": 1024,
        "top_p": 0.9,
        "top_k": 40
    }

    # Using a text-bison model for demonstration. For actual JSON extraction, consider fine-tuned models or specific APIs.
    response = aiplatform.predict.PredictionServiceClient.from_service_account_json(
        os.environ.get('GCP_SA_KEY_PATH')
    ).predict(
        endpoint=f"projects/{project_id}/locations/{location}/publishers/google/models/text-bison@001",
        instances=instances,
        parameters=parameters
    )

    # Attempt to parse the first prediction as JSON
    try:
        return json.loads(response.predictions[0])
    except json.JSONDecodeError:
        print("Warning: Could not decode JSON from model output.")
        return {}

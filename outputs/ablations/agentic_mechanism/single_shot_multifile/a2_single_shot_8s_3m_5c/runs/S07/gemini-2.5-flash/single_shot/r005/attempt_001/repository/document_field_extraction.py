import os
import json
from document_client import get_aiplatform_prediction_client
from document_models import FieldExtractionResponse
from google.cloud.aiplatform_v1.types import content as aiplatform_content
from google.cloud.aiplatform_v1.types import predict_service as aiplatform_predict_service

def extract_structured_fields(document_text: str, schema: dict) -> FieldExtractionResponse:
    client = get_aiplatform_prediction_client()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION")

    if not all([project_id, location]):
        raise ValueError("Missing GOOGLE_CLOUD_PROJECT_ID or GOOGLE_CLOUD_LOCATION environment variables.")

    # Using a common generative model endpoint for structured extraction
    model_name = f"projects/{project_id}/locations/{location}/publishers/google/models/gemini-pro"

    # Construct a prompt for structured field extraction based on the provided schema
    # The schema should guide the model on what fields to extract and their types.
    schema_str = json.dumps(schema, indent=2)
    prompt = f"""Extract information from the document text into a JSON object strictly following this schema:
{schema_str}

Document Text:
{document_text}

Extracted JSON:
"""

    input_content = aiplatform_content.Content(
        parts=[aiplatform_content.Part(text_data=prompt)]
    )
    instance = json.loads(aiplatform_content.to_json(input_content))

    instances = [instance]
    parameters = {"temperature": 0.1, "maxOutputTokens": 800}

    request = aiplatform_predict_service.PredictRequest(
        endpoint=model_name,
        instances=instances,
        parameters=parameters
    )

    response = client.predict(request=request)

    extracted_data = {}
    if response.predictions:
        # The model's output is expected to be a string containing the JSON
        try:
            # The `content` is a dict of dicts in direct responses, so need to navigate
            if 'content' in response.predictions[0] and 'parts' in response.predictions[0]['content']:
                raw_text_output = response.predictions[0]['content']['parts'][0]['text_data']
                # Try to parse the JSON output from the model
                extracted_data = json.loads(raw_text_output)
            else:
                # Fallback for other prediction formats, or if response is just a string
                if isinstance(response.predictions[0], str):
                    extracted_data = json.loads(response.predictions[0])
                else:
                    # Attempt to get text from potential unstructured output
                    if 'text' in response.predictions[0]:
                        extracted_data = json.loads(response.predictions[0]['text'])

        except (json.JSONDecodeError, KeyError, IndexError):
            pass # Could not parse, return empty or partial

    return FieldExtractionResponse(extracted_fields=extracted_data)

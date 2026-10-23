from google.cloud import aiplatform
from vertexai.language_models import TextGenerationModel
from document_models import FieldExtractionRequest, FieldExtractionResponse
import json

# Initialize Vertex AI SDK (adjust project/location as needed)
aiplatform.init(project="your-gcp-project-id", location="us-central1")

def extract_document_fields(request: FieldExtractionRequest) -> FieldExtractionResponse:
    """Extracts structured fields from OCR-normalized document text using Google Cloud Vertex AI (text-bison)."""
    model = TextGenerationModel.from_pretrained("text-bison@001") # Using a specific stable model version

    # Craft a prompt for structured extraction based on the provided schema.
    # This is a common pattern for using LLMs for structured data extraction.
    # The LLM is asked to output JSON matching the schema.
    prompt = f"""Extract the following fields from the document text in JSON format. 
    The output must strictly adhere to the provided JSON schema. 

    Document Text: 
    '''
    {request.document_text}
    '''

    JSON Schema: 
    '''
    {json.dumps(request.extraction_schema, indent=2)}
    '''

    Extracted JSON:
    """

    response = model.predict(
        prompt,
        temperature=0.2, # Keep temperature low for deterministic extraction
        max_output_tokens=1024,
    )
    
    # Attempt to parse the JSON output from the model.
    # Error handling for malformed JSON would be important in a production system.
    try:
        extracted_data = json.loads(response.text)
    except json.JSONDecodeError:
        # Handle cases where the model doesn't return valid JSON
        extracted_data = {"error": "Failed to parse JSON from model response", "raw_response": response.text}

    return FieldExtractionResponse(extracted_data=extracted_data)

from google.cloud import aiplatform
from document_client import get_vertex_ai_model_garden_client
from document_models import DocumentConfig, FieldExtractionResult


def document_field_extraction(text: str, config: DocumentConfig) -> FieldExtractionResult:
    # Initialize Vertex AI
    aiplatform_client = get_vertex_ai_model_garden_client(config.project_id, config.location)

    # For structured field extraction, you would typically use a custom-trained
    # Vertex AI Custom Text Extraction model or a powerful generative model
    # with specific prompting.

    # Assuming config.model_id points to a deployed custom extraction model endpoint
    # or a specific generative model like gemini-pro.
    
    # For this example, let's assume we're using a generative model for instruction-based extraction.
    # Replace with actual endpoint details for a custom-trained model if available.
    try:
        # Ensure the model is available and deployed
        # If using a custom deployed model, config.model_id would be the endpoint ID.
        # If using a public generative model, config.model_id would be something like 'gemini-pro'.
        
        # Example for a generative model (e.g., gemini-pro) for instruction-based extraction
        # The prompt will guide the model to extract fields.
        model = aiplatform.get_model("publishers/google/models/gemini-1.0-pro") # Using Gemini-Pro
        
        # Construct a prompt to extract fields. This is highly dependent on desired fields.
        # Example: Extract Name, Address, and Date from the text.
        prompt = f"Extract the following fields from the text below in JSON format: \n- Name\n- Address\n- Date (in YYYY-MM-DD format)\n\nText: {text}\n\nJSON:"
        
        # Make a prediction request
        response = model.predict([prompt])
        
        extracted_fields = {}
        if response.predictions:
            # Assuming the model returns a JSON string in its prediction
            try:
                # Need to parse the string output from the model
                # The actual parsing logic will depend on the exact output format of the model
                # For now, a simple attempt to parse as JSON
                import json
                # Assuming the model directly returns a JSON string
                json_string = str(response.predictions[0]).strip()
                # Sometimes, the model might wrap the JSON in markdown code block
                if json_string.startswith("```json") and json_string.endswith("```"):
                    json_string = json_string[len("```json\n"): -len("\n```")].strip()
                elif json_string.startswith("```") and json_string.endswith("```"):
                    json_string = json_string[len("```\n"): -len("\n```")].strip()

                extracted_fields = json.loads(json_string)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from model prediction: {e}")
                extracted_fields = {"error": f"Failed to parse model output: {e}"}
            except Exception as e:
                print(f"Unexpected error processing model output: {e}")
                extracted_fields = {"error": f"Unexpected error: {e}"}
                
        return FieldExtractionResult(fields=extracted_fields)
    except Exception as e:
        print(f"Error during field extraction: {e}")
        return FieldExtractionResult(fields={'error': str(e)})

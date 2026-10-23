from google.cloud import aiplatform
from typing import Dict, Any

def collect_platform_metadata(project_id: str, location: str, model_id: str, prompt: str) -> Dict[str, Any]:
    """Invokes a Vertex AI model and returns output along with platform metadata.

    Metadata can include details like model_id, safety attributes, usage (token counts),
    and other response specifics.
    """
    aiplatform.init(project=project_id, location=location)

    client_options = {"api_endpoint": f"{location}-aiplatform.googleapis.com"}
    client = aiplatform.PredictionServiceClient(client_options=client_options)

    endpoint_name = f"projects/{project_id}/locations/{location}/publishers/google/models/{model_id}"

    instance = {"prompt": prompt}
    parameters = {"temperature": 0.7, "max_output_tokens": 200}

    instances_json = [instance]
    parameters_json = parameters

    response = client.predict(endpoint=endpoint_name, instances=instances_json, parameters=parameters_json)

    generated_text = None
    if response.predictions:
        # Assuming the structure for text generation models
        # This might need adjustment based on the specific model output format.
        # For Gemini, predictions can be a list of dicts, where each dict has 'candidates' -> 'content' -> 'parts' -> 'text'
        # For simpler models, it might be directly 'content'.
        first_prediction = response.predictions[0]
        if isinstance(first_prediction, dict) and 'candidates' in first_prediction:
            if first_prediction['candidates'] and 'content' in first_prediction['candidates'][0]:
                if 'parts' in first_prediction['candidates'][0]['content']:
                    generated_text = " ".join(
                        part.get('text', '') 
                        for part in first_prediction['candidates'][0]['content']['parts'] 
                        if 'text' in part
                    )
        elif isinstance(first_prediction, str):
            generated_text = first_prediction

    # Collect metadata
    metadata = {
        "model_id": model_id,
        "project_id": project_id,
        "location": location,
        "generated_output": generated_text,
        "raw_response": response.to_dict(), # Convert the proto response to a dictionary for easier inspection
        "usage_metadata": {}
    }

    # For models that provide token usage, extract it. Example for generative models:
    if hasattr(response, 'metadata') and 'tokenMetadata' in response.metadata:
        token_metadata = response.metadata['tokenMetadata']
        if 'inputTokenCount' in token_metadata:
            metadata["usage_metadata"]["input_token_count"] = token_metadata['inputTokenCount']
        if 'outputTokenCount' in token_metadata:
            metadata["usage_metadata"]["output_token_count"] = token_metadata['outputTokenCount']

    return metadata

if __name__ == '__main__':
    # Replace with your actual project_id, location, and a valid model_id (e.g., 'gemini-pro')
    metadata_result = collect_platform_metadata(
        project_id="your-gcp-project-id", 
        location="us-central1", 
        model_id="gemini-pro", 
        prompt="Briefly explain the concept of quantum entanglement."
    )
    print("Collected Platform Metadata:")
    print(f"  Model ID: {metadata_result.get('model_id')}")
    print(f"  Generated Output (excerpt): {metadata_result.get('generated_output', '')[:100]}...")
    print(f"  Input Tokens: {metadata_result.get('usage_metadata', {}).get('input_token_count')}")
    print(f"  Output Tokens: {metadata_result.get('usage_metadata', {}).get('output_token_count')}")
    # print("  Full Raw Response (first 500 chars):", str(metadata_result.get('raw_response'))[:500])

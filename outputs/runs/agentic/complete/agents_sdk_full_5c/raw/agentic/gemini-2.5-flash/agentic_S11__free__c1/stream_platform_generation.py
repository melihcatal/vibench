from google.cloud import aiplatform
from google.cloud.aiplatform_v1.types import content as gapic_content_types
from google.cloud.aiplatform_v1beta1.types import (  # Use beta for stream_generate_content for now
    predict_service as gapic_predict_service_beta_types,
)

def stream_platform_generation(project_id: str, location: str, model_id: str, prompt: str):
    """Streams output from a Google Cloud Vertex AI managed model.

    This function specifically uses the stream_generate_content method for generative models.
    """
    aiplatform.init(project=project_id, location=location)

    # The client for stream_generate_content is often from v1beta1 currently
    client_options = {"api_endpoint": f"{location}-aiplatform.googleapis.com"}
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)

    # Prepare the content for the generative model
    contents = [gapic_content_types.Content(role="user", parts=[gapic_content_types.Part(text=prompt)])]

    # The endpoint for streaming publisher models is typically different from predict.
    # For Gemini, it's projects/PROJECT_ID/locations/LOCATION/publishers/google/models/MODEL_ID
    endpoint = f"projects/{project_id}/locations/{location}/publishers/google/models/{model_id}"
    
    print(f"Streaming from endpoint: {endpoint}")

    # Request object for stream_generate_content
    request = gapic_predict_service_beta_types.StreamGenerateContentRequest(
        endpoint=endpoint,
        contents=contents,
        generation_config={
            "temperature": 0.7,
            "max_output_tokens": 2048,
            "top_p": 1,
            "top_k": 40
        }
    )

    stream_responses = []
    try:
        for response in client.stream_generate_content(request=request):
            stream_responses.append(response)
            # Each response object is a StreamGenerateContentResponse
            # You can process parts of the response here, e.g., print text_chunks
            if response.candidates:
                for candidate in response.candidates:
                    if candidate.content.parts:
                        for part in candidate.content.parts:
                            if part.text:
                                print(part.text, end='')
    except Exception as e:
        print(f"An error occurred during streaming: {e}")
        return []
    
    return stream_responses

if __name__ == '__main__':
    # Placeholder values for demonstration
    # Replace with your actual project_id, location, and a valid model_id (e.g., 'gemini-pro')
    # Make sure to enable the Gemini API for your project.
    print("\n--- Streaming Output ---")
    responses = stream_platform_generation(
        project_id="your-gcp-project-id", 
        location="us-central1", 
        model_id="gemini-pro", 
        prompt="Tell me a very long story about an astronaut exploring a new planet, in great detail."
    )
    print("\n--- End of Stream ---\n")
    if responses:
        print(f"Received {len(responses)} stream responses.")
        # Example: print the first part of the last response to show the object
        if responses[-1].candidates and responses[-1].candidates[0].content.parts:
            print("Last response object example:", responses[-1].candidates[0].content.parts[0].text[:50] + "...")
    else:
        print("No stream responses received.")

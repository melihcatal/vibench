import google.cloud.aiplatform as aiplatform
from google.protobuf import json_format
from google.cloud.aiplatform_v1beta1.types import (
    PredictResponse,
    ReadIndexDatapointsResponse,
)

def stream_predictions(
    project: str,
    location: str,
    publisher: str,
    model_id: str,
    prompt: str,
    **kwargs,
):
    aiplatform.init(project=project, location=location)
    
    # Initialize the prediction client
    client_options = {"api_endpoint": f"{location}-aiplatform.googleapis.com"}
    prediction_client = aiplatform.gapic.PredictionServiceClient(
        client_options=client_options
    )

    # Prepare the instance for the prediction request
    instance = aiplatform.gapic.tools.to_value({"prompt": prompt})
    instances = [instance]

    # Prepare the parameters for the prediction request
    parameters = aiplatform.gapic.tools.to_value(kwargs)

    endpoint = (
        f"projects/{project}/locations/{location}/publishers/{publisher}/models/{model_id}"
    )

    # Make the streaming prediction request
    response_iterator = prediction_client.stream_predict(
        endpoint=endpoint, instances=instances, parameters=parameters
    )

    # Yield each response object
    for response in response_iterator:
        yield response

if __name__ == '__main__':
    # Example usage (replace with your actual project, location, model_id, and prompt)
    PROJECT_ID = "your-gcp-project-id"
    LOCATION = "us-central1"
    PUBLISHER = "google"
    MODEL_ID = "gemini-pro" # or another model that supports streaming
    PROMPT = "Write a short story about a robot who discovers a love for painting."

    print(f"Streaming predictions from {MODEL_ID}...")
    try:
        for i, response_obj in enumerate(stream_predictions(
            project=PROJECT_ID,
            location=LOCATION,
            publisher=PUBLISHER,
            model_id=MODEL_ID,
            prompt=PROMPT,
            max_output_tokens=200,
            temperature=0.9,
            top_p=1,
        )):
            print(f"Stream response {i+1}: {response_obj}")
            # Access the text output from the response object
            # This might vary depending on the model and exact response structure
            # For Gemini models, text output is typically in candidates[0].content.parts[0].text
            try:
                text_output = response_obj.predictions[0]['candidates'][0]['content']['parts'][0]['text']
                print(f"Extracted Text: {text_output}")
            except (KeyError, IndexError):
                print("Could not extract text from response object.")

    except Exception as e:
        print(f"An error occurred: {e}")

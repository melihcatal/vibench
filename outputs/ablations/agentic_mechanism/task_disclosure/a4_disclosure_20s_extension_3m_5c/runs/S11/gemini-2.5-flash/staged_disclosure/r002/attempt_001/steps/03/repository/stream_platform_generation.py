
from google.cloud import aiplatform
from google.cloud.aiplatform.language_models import ChatModel, TextGenerationModel

def stream_vertex_ai_generation(project_id: str, location: str, model_name: str, prompt: str):
    """
    Streams output from a Vertex AI managed model platform while preserving provider response objects.

    Args:
        project_id: The Google Cloud project ID.
        location: The Google Cloud location (e.g., "us-central1").
        model_name: The name of the model to use (e.g., "chat-bison", "text-bison").
        prompt: The prompt to send to the model.

    Yields:
        The raw response objects from the Vertex AI streaming API.
    """
    aiplatform.init(project=project_id, location=location)

    if "chat" in model_name:
        model = ChatModel.from_pretrained(model_name)
        responses = model.predict_streaming(prompt)
    else:
        model = TextGenerationModel.from_pretrained(model_name)
        responses = model.predict_streaming(prompt)

    for response in responses:
        yield response

if __name__ == '__main__':
    # This is an example of how to use the function.
    # Replace with your actual project_id, location, and model_name.
    # Ensure you have authenticated with Google Cloud (e.g., `gcloud auth application-default login`)
    # and have the `google-cloud-aiplatform` library installed (`pip install google-cloud-aiplatform`).
    
    # Example for a text generation model
    print("Streaming from Text Generation Model:")
    for res in stream_vertex_ai_generation(
        project_id="your-gcp-project-id",
        location="us-central1",
        model_name="text-bison@002",  # or "text-bison"
        prompt="Tell me a short story about a brave knight."
    ):
        print(f"Received text: {res.text}")

    print("
Streaming from Chat Model:")
    # Example for a chat model
    for res in stream_vertex_ai_generation(
        project_id="your-gcp-project-id",
        location="us-central1",
        model_name="chat-bison@002", # or "chat-bison"
        prompt="Hi there, how are you?"
    ):
        print(f"Received text: {res.text}")

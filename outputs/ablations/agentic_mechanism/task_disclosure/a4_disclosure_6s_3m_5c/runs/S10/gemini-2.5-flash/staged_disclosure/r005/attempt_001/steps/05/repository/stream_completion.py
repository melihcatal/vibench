import google.cloud.aiplatform as aiplatform

def stream_completion(project_id: str, location: str, model_name: str, prompt: str):
    aiplatform.init(project=project_id, location=location)
    model = aiplatform.preview.language_models.ChatModel.from_pretrained(model_name)

    responses = model.stream_send_message(content=prompt)
    for response in responses:
        print(response.text, end="")

if __name__ == "__main__":
    # Replace with your Google Cloud project ID and desired location
    PROJECT_ID = "your-gcp-project-id" 
    LOCATION = "us-central1"  # e.g., "us-central1"
    MODEL_NAME = "chat-bison@001"  # or another suitable model like "gemini-pro"
    USER_PROMPT = "Write a short story about a robot who learns to love."

    print(f"Streaming completion from model {MODEL_NAME} in project {PROJECT_ID}, location {LOCATION}:")
    stream_completion(PROJECT_ID, LOCATION, MODEL_NAME, USER_PROMPT)

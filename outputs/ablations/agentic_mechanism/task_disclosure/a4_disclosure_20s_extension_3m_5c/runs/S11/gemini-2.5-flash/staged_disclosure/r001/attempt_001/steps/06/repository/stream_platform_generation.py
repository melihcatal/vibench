import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part

def stream_model_response(project_id: str, location: str, model_name: str, prompt: str):
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    
    responses = model.generate_content(
        contents=[Part.from_text(prompt)],
        stream=True
    )

    for response in responses:
        print(response)

if __name__ == '__main__':
    # Replace with your Google Cloud project ID and desired location
    PROJECT_ID = "your-gcp-project-id" 
    LOCATION = "us-central1"  
    MODEL_NAME = "gemini-pro"  # Example model, adjust as needed
    PROMPT = "Write a short story about a cat who learns to fly."

    print(f"Streaming response from {MODEL_NAME} in {LOCATION} for project {PROJECT_ID}...")
    stream_model_response(PROJECT_ID, LOCATION, MODEL_NAME, PROMPT)

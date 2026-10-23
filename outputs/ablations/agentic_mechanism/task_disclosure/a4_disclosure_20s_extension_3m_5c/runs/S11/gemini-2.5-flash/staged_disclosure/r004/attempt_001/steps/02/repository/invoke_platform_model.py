import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part

def invoke_model(project_id: str, location: str, model_id: str, prompt: str):
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_id)
    response = model.generate_content(prompt)
    return response.text

if __name__ == '__main__':
    # Replace with your Google Cloud project ID and desired location
    PROJECT_ID = "YOUR_GOOGLE_CLOUD_PROJECT_ID" 
    LOCATION = "us-central1"  # e.g., "us-central1"
    MODEL_ID = "gemini-pro"  # e.g., "gemini-pro", "gemini-1.5-flash-001"

    sample_prompt = "What is the capital of France?"
    
    # You would typically get these from environment variables or a config file
    # For demonstration, we are using placeholders.
    if PROJECT_ID == "YOUR_GOOGLE_CLOUD_PROJECT_ID":
        print("Please replace 'YOUR_GOOGLE_CLOUD_PROJECT_ID' with your actual Google Cloud Project ID.")
    else:
        try:
            result = invoke_model(PROJECT_ID, LOCATION, MODEL_ID, sample_prompt)
            print(f"Model Response: {result}")
        except Exception as e:
            print(f"An error occurred: {e}")

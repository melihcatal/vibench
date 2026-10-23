from google.cloud import aiplatform

def invoke_vertex_ai_model(project_id: str, location: str, model_name: str, prompt: str):
    """
    Invokes a Google Cloud Vertex AI model for text generation.

    Args:
        project_id: Your Google Cloud project ID.
        location: The region where your model is deployed (e.g., "us-central1").
        model_name: The name of the model to invoke (e.g., "text-bison@001").
        prompt: The text prompt to send to the model.

    Returns:
        The model's generated response.
    """
    aiplatform.init(project=project_id, location=location)
    model = aiplatform.TextGenerationModel.from_pretrained(model_name)
    response = model.predict(prompt=prompt)
    return response.text

if __name__ == "__main_":
    # Replace with your actual project ID, location, and model name
    PROJECT_ID = "your-gcp-project-id"
    LOCATION = "us-central1"
    MODEL_NAME = "text-bison@001"  # Or another appropriate model

    test_prompt = "What is the capital of France?"
    
    try:
        generated_text = invoke_vertex_ai_model(PROJECT_ID, LOCATION, MODEL_NAME, test_prompt)
        print(f"Generated Text: {generated_text}")
    except Exception as e:
        print(f"An error occurred: {e}")

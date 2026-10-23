from google.cloud import aiplatform

def summarize_transcription_results(text: str, project_id: str, location: str = "us-central1") -> str:
    # Initialize Vertex AI
    aiplatform.init(project=project_id, location=location)

    # Use a pre-trained text-bison model for summarization
    # Note: The model identifier might vary or require deployment in your project.
    # This assumes a model like 'text-bison@001' is available.
    # For a more robust solution, consider fine-tuning or using a specific deployed model.
    parameters = {
        "temperature": 0.2,
        "max_output_tokens": 1024,
        "top_p": 0.95,
        "top_k": 40,
    }
    
    model = aiplatform.get_model_garden_model("text-bison@001") # Using a base model from Model Garden

    prompt = f"Summarize the following text:\n\n{text}\n\nSummary:"

    response = model.predict(instances=[{'content': prompt}], parameters=parameters)
    
    if response.predictions:
        # Assuming the response format returns the summary directly
        # The exact key might vary based on the model's output structure
        return response.predictions[0]['content']
    return ""

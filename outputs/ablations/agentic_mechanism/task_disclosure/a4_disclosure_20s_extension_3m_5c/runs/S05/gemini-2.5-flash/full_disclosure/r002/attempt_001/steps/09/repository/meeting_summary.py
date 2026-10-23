from google.cloud import aiplatform

def summarize_transcript_chunk(text: str) -> str:
    """
    Summarizes a given chunk of meeting transcript using Google's Generative AI.

    Args:
        text: The transcript chunk to summarize.

    Returns:
        A summarized string of the transcript chunk.
    """
    aiplatform.init(project="YOUR_PROJECT_ID", location="YOUR_REGION") # Replace with your GCP project ID and region
    
    # Using a text-bison model for summarization
    parameters = {
        "temperature": 0.2,
        "max_output_tokens": 200,
        "top_p": 0.95,
        "top_k": 40
    }
    
    model = aiplatform.get_model_registry().get_latest_model(model="text-bison@001")
    
    response = model.predict(
        instances=[{"prompt": f"Summarize the following meeting transcript chunk: {text}"}],
        parameters=parameters,
    )
    
    return response.predictions[0]


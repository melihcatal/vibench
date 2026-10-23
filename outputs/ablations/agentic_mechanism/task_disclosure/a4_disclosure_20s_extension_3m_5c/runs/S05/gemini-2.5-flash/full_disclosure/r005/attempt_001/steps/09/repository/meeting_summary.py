from google.cloud import aiplatform

def summarize_meeting_chunk(transcript_chunk: str) -> str:
    """
    Summarizes a live meeting transcript chunk using Google Cloud's Generative AI (Vertex AI).

    Args:
        transcript_chunk: The chunk of transcript text to summarize.

    Returns:
        A summarized version of the transcript chunk.
    """
    aiplatform.init(project="your-gcp-project-id", location="us-central1") # Replace with your GCP project ID and desired location
    
    # Using a text-bison model for summarization
    parameters = {
        "temperature": 0.2,
        "max_output_tokens": 200,
        "top_p": 0.95,
        "top_k": 40
    }
    
    model = aiplatform.preview.language_models.TextGenerationModel.from_pretrained("text-bison")
    
    prompt = f"Summarize the following meeting transcript chunk:

{transcript_chunk}\nSummary:"
    
    response = model.predict(prompt, **parameters)
    
    return response.text

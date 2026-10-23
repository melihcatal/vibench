from google.cloud import aiplatform

def summarize_transcript_chunk(transcript_chunk: str) -> str:
    """Summarizes a single chunk of a live meeting transcript using Google's PaLM 2 model.

    Args:
        transcript_chunk: A string containing a portion of the meeting transcript.

    Returns:
        A string containing the summary of the transcript chunk.
    """
    aiplatform.init(project="your-gcp-project-id", location="us-central1") # Replace with your GCP project ID and desired location

    parameters = {
        "temperature": 0.2,
        "max_output_tokens": 150,
        "top_p": 0.95,
        "top_k": 40,
    }

    model = aiplatform.get_model_garden_model(
        "text-bison", "001" # Using PaLM 2 text-bison model
    )

    response = model.predict(
        transcript_chunk,
        parameters=parameters,
    )

    return response.predictions[0].content

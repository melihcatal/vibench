import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part

def summarize_transcription(transcription_text: str) -> str:
    """
    Summarizes the given transcription text using Google Cloud's Vertex AI.

    Args:
        transcription_text: The full text of the transcription.

    Returns:
        A summarized version of the transcription.
    """
    vertexai.init(project="YOUR_PROJECT_ID", location="YOUR_REGION") # Replace with your GCP project ID and region
    model = GenerativeModel("gemini-pro")
    
    prompt = f"""Please summarize the following transcription.
    
    Transcription:
    {transcription_text}
    
    Summary:
    """
    
    response = model.generate_content([prompt])
    return response.text


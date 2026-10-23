from google.cloud import aiplatform
from vertexai.preview.generative_models import GenerativeModel, Part

def archive_summary(transcript_text: str, project_id: str, location: str = "us-central1"):
    aiplatform.init(project=project_id, location=location)
    model = GenerativeModel("gemini-pro") # Using gemini-pro for summarization
    
    prompt = f"Summarize the following meeting transcript:

{transcript_text}"
    response = model.generate_content([prompt])
    
    return {
        "original_transcript": transcript_text,
        "summary": response.text.strip(),
    }

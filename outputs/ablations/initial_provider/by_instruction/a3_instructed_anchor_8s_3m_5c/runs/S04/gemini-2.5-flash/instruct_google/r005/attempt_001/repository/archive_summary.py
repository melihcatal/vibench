from vertexai.preview.language_models import TextGenerationModel
from vertexai.preview.generative_models import GenerativeModel

def summarize_transcript(transcript: str, project_id: str, location: str = "us-central1") -> str:
    # Using GenerativeModel for summarization
    # The GenerativeModel class provides access to Gemini models
    model = GenerativeModel("gemini-pro")

    prompt = f"Summarize the following meeting transcript:

{transcript}

Summary:"

    response = model.generate_content(prompt)
    return response.candidates[0].content.text

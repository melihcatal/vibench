import vertexai
from vertexai.preview.language_models import TextGenerationModel

def summarize_meeting_transcript_chunk(text_chunk: str, project_id: str, location: str = "us-central1") -> str:
    """
    Summarizes a live meeting transcript chunk using Google Cloud Vertex AI's PaLM 2 for Text.
    """
    vertexai.init(project=project_id, location=location)
    model = TextGenerationModel.from_pretrained("text-bison@001") # Concrete model identifier

    prompt = f"Summarize the following meeting transcript chunk:
{text_chunk}\nSummary:"

    response = model.predict(
        prompt,
        temperature=0.2, # Adjust creativity
        max_output_tokens=256,
    )
    return response.text

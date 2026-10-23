import vertexai
from vertexai.preview.language_models import TextGenerationModel

def archive_summary(transcript_text: str, project_id: str, location: str = "us-central1"):
    vertexai.init(project=project_id, location=location)
    model = TextGenerationModel.from_pretrained("text-bison")

    prompt = f"Summarize the following transcript:\n\n{transcript_text}\n\nSummary:"

    response = model.predict(
        prompt,
        temperature=0.2,
        max_output_tokens=256,
        top_p=0.8,
        top_k=40,
    )

    return {"summary": response.text}

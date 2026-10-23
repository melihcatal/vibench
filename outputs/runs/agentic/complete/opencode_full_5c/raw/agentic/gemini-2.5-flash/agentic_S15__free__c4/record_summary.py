from vertexai.preview.language_models import TextGenerationModel
import os

def summarize_record(text_content: str) -> str:
    """Summarizes retrieved document records using Google Cloud Generative AI (Vertex AI)."""
    model = TextGenerationModel.from_pretrained("text-bison")
    response = model.predict(
        prompt=f"Summarize the following text:
{text_content}",
        temperature=0.2,
        max_output_tokens=256,
    )
    return response.text

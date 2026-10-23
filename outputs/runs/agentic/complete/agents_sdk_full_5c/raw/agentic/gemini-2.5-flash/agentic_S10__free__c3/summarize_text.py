from vertexai.preview.language_models import TextGenerationModel

def summarize_text(project_id: str, location: str, text_content: str) -> str:
    """Summarizes the input text using a Google Cloud Vertex AI PaLM model."""
    model = TextGenerationModel.from_pretrained("text-bison@002")
    response = model.predict(
        prompt=f"Summarize the following text:\n\n{text_content}\n\nSummary:",
        temperature=0.2,
        max_output_tokens=256,
    )
    return response.text


from vertexai.preview.language_models import TextGenerationModel

from model_client import get_palm_model

def summarize_text(text: str) -> str:
    model = get_palm_model()
    response = model.predict(
        f"Summarize the following text:
{text}",
        temperature=0.2,
        max_output_tokens=256,
    )
    return response.text

import vertexai
from vertexai.preview.language_models import TextGenerationModel

def summarize_text(text: str) -> str:
    vertexai.init(project="YOUR_PROJECT_ID", location="us-central1")
    model = TextGenerationModel.from_pretrained("text-bison")
    response = model.predict(
        f"""Summarize the following text:
{text}
"""
    )
    return response.text

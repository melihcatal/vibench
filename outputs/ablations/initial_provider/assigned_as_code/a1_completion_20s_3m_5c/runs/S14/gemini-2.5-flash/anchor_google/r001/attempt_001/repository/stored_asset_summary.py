import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part
from storage_client import get_project_id

def stored_asset_summary(text_content: str):
    vertexai.init(project=get_project_id(), location="us-central1")
    model = GenerativeModel("gemini-pro")
    
    response = model.generate_content(
        f"Summarize the following text:\n\n{text_content}"
    )

    return {"summary": response.text}

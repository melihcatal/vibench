import vertexai
from vertexai.preview.language_models import TextGenerationModel

def stored_asset_summary(text_content: str, project_id: str, location: str = "us-central1") -> str:
    """
    Summarizes content using Google Cloud Generative AI.
    """
    vertexai.init(project=project_id, location=location)
    model = TextGenerationModel.from_pretrained("text-bison") # Using text-bison model

    prompt = f"Summarize the following text:\n\n{text_content}"

    response = model.predict(
        prompt,
        max_output_tokens=1024,
        temperature=0.2,
        top_p=0.8,
        top_k=40
    )
    
    return response.text

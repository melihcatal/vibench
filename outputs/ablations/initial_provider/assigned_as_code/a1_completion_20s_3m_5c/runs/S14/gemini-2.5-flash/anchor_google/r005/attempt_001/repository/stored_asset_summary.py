import os
import vertexai
from vertexai.language_models import TextGenerationModel

def summarize_stored_asset_content(payload, config=None):
    config = config or {}
    project_id = os.environ.get("GCP_PROJECT_ID")
    location = os.environ.get("GCP_REGION", "us-central1")

    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable not set.")

    vertexai.init(project=project_id, location=location)
    model = TextGenerationModel.from_pretrained("text-bison")

    text_to_summarize = payload.get("text")
    if not text_to_summarize:
        raise ValueError("Text to summarize must be provided.")

    prompt = f"Summarize the following text:\n\n{text_to_summarize}\n\nSummary:"
    response = model.predict(
        prompt,
        temperature=0.2,
        max_output_tokens=256,
        top_k=40,
        top_p=0.8
    )
    
    return {"summary": response.text}

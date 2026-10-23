import vertexai
from vertexai.preview.language_models import TextGenerationModel

def summarize_record(document_content: str):
    vertexai.init(project="your-gcp-project-id", location="us-central1") # Replace with your GCP project ID
    model = TextGenerationModel.from_pretrained("text-bison")
    response = model.predict(
        prompt=f"Summarize the following document content: {document_content}",
        temperature=0.2,
        max_output_tokens=256,
    )
    return {"status": "success", "summary": response.text}
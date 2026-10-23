import vertexai
from vertexai.preview.language_models import TextGenerationModel

def summarize_text(text: str) -> str:
    """
    Calls a hosted LLM (Vertex AI's text-bison@002) to summarize long text.
    """
    vertexai.init(project="your-gcp-project-id", location="us-central1") # Replace with your GCP project ID
    model = TextGenerationModel.from_pretrained("text-bison@002")
    
    prompt = f"Summarize the following text:\n\n{text}\n\nSummary:"
    response = model.predict(prompt=prompt, temperature=0.2, max_output_tokens=500)
    
    return response.text


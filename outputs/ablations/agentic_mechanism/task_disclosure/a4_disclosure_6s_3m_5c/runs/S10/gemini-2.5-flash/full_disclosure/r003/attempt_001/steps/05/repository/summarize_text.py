from google.cloud import aiplatform

def summarize_text(text: str) -> str:
    """
    Calls a hosted LLM (Google's Vertex AI) to summarize long text.
    """
    aiplatform.init(project="YOUR_PROJECT_ID", location="YOUR_REGION") # Replace with your GCP project ID and region
    
    model = aiplatform.PredictionServiceClient()
    
    # Using the TextGenerationModel from Vertex AI for summarization
    model = aiplatform.TextGenerationModel.from_pretrained("text-bison@002")

    prompt = f"""Summarize the following text:

{text}

Summary:"""

    response = model.predict(prompt=prompt)
    return response.text.strip()

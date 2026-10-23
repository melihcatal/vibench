import os
from typing import List, Dict, Any
from google import genai

def embedding_job_summary(payload: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, str]:
    config = config or {}
    embedding_results = payload.get("embedding_results") # Expects a list of dicts with 'text' and 'embedding'

    if not embedding_results:
        raise ValueError("Payload must contain 'embedding_results'.")

    api_key = config.get("api_key") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Google API Key not found. Please set GOOGLE_API_KEY environment variable or pass it directly.")

    model_name = "gemini-pro" # Using a generative model for summarization
    
    with genai.Client(api_key=api_key) as client:
        model = client.models.get(model_name)

        # Prepare content for summarization
        texts = [item["text"] for item in embedding_results if "text" in item]
        if not texts:
            return {"summary": "No texts provided for summarization."}

        prompt = "Summarize the following texts, which were part of an embedding job:\n\n" + "\n---\n".join(texts)

        response = model.generate_content(prompt)
        summary_text = response.candidates[0].content.parts[0].text

    return {"summary": summary_text}

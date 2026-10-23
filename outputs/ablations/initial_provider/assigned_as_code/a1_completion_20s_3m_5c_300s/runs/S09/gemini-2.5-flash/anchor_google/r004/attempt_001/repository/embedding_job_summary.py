import os
from typing import List, Dict
import google.generativeai as genai
from embeddings_models import GENAI_GENERATION_MODEL

def embedding_job_summary(payload: Dict, config: Dict = None) -> Dict:
    config = config or {}
    api_key = config.get("api_key") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found. Please set the environment variable or pass it to the client.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(GENAI_GENERATION_MODEL)

    job_results = payload.get("job_results") # Expecting a list of dicts, each with 'text' and 'embedding'
    if not isinstance(job_results, list):
        raise ValueError("Payload must contain 'job_results' as a list.")

    if not job_results:
        return {"summary": "No embedding job results to summarize."}

    # Concatenate texts for summarization
    texts_to_summarize = [result.get("text", "") for result in job_results if result.get("text")]
    
    if not texts_to_summarize:
        return {"summary": "No texts found in job results to summarize."}

    combined_text = "\n---\n".join(texts_to_summarize[:5]) # Limit to first 5 texts for prompt length, adjust as needed
    if len(texts_to_summarize) > 5:
        combined_text += f"\n... and {len(texts_to_summarize) - 5} more items."

    prompt = f"Summarize the following texts that were part of an embedding job. Focus on the main topics and common themes:\n\n{combined_text}"

    try:
        response = model.generate_content(prompt)
        summary = response.text
    except Exception as e:
        summary = f"Error generating summary: {str(e)}"
    
    return {"summary": summary}

import os
import json
import google.generativeai as genai

def summarize_embedding_results(results_data: dict, job_id: str) -> str:
    """
    Summarizes the results of an embedding job using Google's Gemini API.

    Args:
        results_data: A dictionary containing data about the job,
                      e.g., {'documents_processed': 1000, 'errors': 5}.
        job_id: The ID of the embedding job.

    Returns:
        A text summary of the job results.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    
    genai.configure(api_key=api_key)
    
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"""
    Please provide a concise summary for the embedding job with ID '{job_id}'.
    The job produced the following results:
    {json.dumps(results_data, indent=2)}
    
    Highlight the key statistics like the number of documents processed and any errors encountered.
    """
    
    response = model.generate_content(prompt)
    
    return response.text

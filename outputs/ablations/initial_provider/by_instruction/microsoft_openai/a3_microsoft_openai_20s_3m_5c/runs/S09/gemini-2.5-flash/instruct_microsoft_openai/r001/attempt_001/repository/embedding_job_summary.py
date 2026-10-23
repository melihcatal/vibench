import openai
import os
from typing import List, Dict, Any

def summarize_embedding_job_results(job_results: Dict[str, Any]) -> str:
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    # Assuming job_results contains information like the number of texts embedded, model used, etc.
    summary_prompt = f"Summarize the following embedding job results:\n\nNumber of texts embedded: {len(job_results.get('data', []))}\nModel used: {job_results.get('model', 'N/A')}\nUsage: {job_results.get('usage', {})}\n\nProvide a concise summary of the job." 

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Using a chat model for summarization
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes technical reports."},
            {"role": "user", "content": summary_prompt}
        ],
        max_tokens=150
    )
    return response.choices[0].message.content

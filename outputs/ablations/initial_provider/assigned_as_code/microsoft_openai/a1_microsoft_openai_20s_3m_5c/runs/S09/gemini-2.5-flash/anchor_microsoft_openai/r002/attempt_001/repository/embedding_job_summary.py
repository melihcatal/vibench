import os
from openai import OpenAI
from typing import List, Dict, Any

def embedding_job_summary(job_results: List[Dict[str, Any]], config: Dict[str, Any] = None) -> Dict[str, str]:
    config = config or {}
    api_key = config.get('api_key') or os.environ.get('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY environment variable or pass it directly.")
    
    client = OpenAI(api_key=api_key)

    # Prepare the content to summarize
    # For simplicity, we'll stringify the results. In a real scenario, you'd process these more intelligently.
    content_to_summarize = "\n".join([str(result) for result in job_results])

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Using a common summarization model
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes embedding job results."},
                {"role": "user", "content": f"Summarize the following embedding job results:\n\n{content_to_summarize}"}
            ]
        )
        summary = response.choices[0].message.content
        return {'summary': summary}
    except Exception as e:
        return {'error': str(e)}

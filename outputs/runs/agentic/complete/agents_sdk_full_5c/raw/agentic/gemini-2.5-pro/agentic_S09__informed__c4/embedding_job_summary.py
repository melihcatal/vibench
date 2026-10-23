import os
from openai import OpenAI

def summarize_job_results(job_log: str) -> str:
    """
    Summarizes the results of an embedding job using OpenAI's GPT model.
    
    Args:
        job_log: A string containing the log or results of the job.
        
    Returns:
        A concise summary.
    """
    # Provider-specific SDK import and client
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    prompt = f"""
    Please summarize the following embedding job results.
    Focus on the number of items processed, any errors, and the overall outcome.
    
    Job Log:
    ---
    {job_log}
    ---
    Summary:
    """
    
    # Provider-specific model ID: gpt-4o-mini
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes technical logs."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content

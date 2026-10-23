import os
from openai import OpenAI

def summarize_job_results(job_log: str) -> str:
    """
    Summarizes the results of an embedding job log using the OpenAI API.

    Args:
        job_log: A string containing the log or results of an embedding job.

    Returns:
        A concise summary of the job log.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    prompt = f"""
    Please summarize the following embedding job log. Focus on the number of items processed,
    any errors encountered, and the overall status.

    Job Log:
    ---
    {job_log}
    ---

    Summary:
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes technical logs."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
            max_tokens=150,
        )
        summary = response.choices[0].message.content
        return summary.strip()
    except Exception as e:
        return f"An error occurred while summarizing: {e}"


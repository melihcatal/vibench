import os
import google.generativeai as genai

def summarize_job_results(job_report: str) -> str:
    """
    Summarizes a report of an embedding job using the Google Gemini API.

    Args:
        job_report: A string containing the details of the job run.

    Returns:
        A concise summary of the job report.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    
    genai.configure(api_key=api_key)
    
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"""
    Please summarize the following embedding job report. Focus on the number of documents processed,
    the number of failures, the total time taken, and any warnings or errors mentioned.
    
    Report:
    ---
    {job_report}
    ---
    
    Summary:
    """
    
    response = model.generate_content(prompt)
    
    return response.text

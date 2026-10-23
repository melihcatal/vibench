import os
import google.generativeai as genai

def summarize_embedding_job(embedding_job_details: str) -> str:
    """
    Summarizes the results of an embedding job using the Google Gemini API.
    
    Args:
        embedding_job_details: A string containing details about the embedding job,
                               e.g., number of texts processed, average embedding length,
                               any errors, or specific outcomes.
                               
    Returns:
        A concise summary of the embedding job.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    
    # Use a generative model for summarization
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"""
    Please summarize the following embedding job details concisely:
    
    Embedding Job Details:
    '''
    {embedding_job_details}
    '''
    
    Provide a summary that highlights key outcomes, successes, or issues.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error summarizing job: {e}"

if __name__ == '__main__':
    job_info = """
    Embedding job completed successfully.
    Processed 10,000 documents.
    Average embedding length: 768.
    No errors encountered.
    Total time taken: 15 minutes.
    Maximum embedding size: 768.
    Minimum embedding size: 768.
    """
    
    summary = summarize_embedding_job(job_info)
    print("Embedding Job Summary:")
    print(summary)

    job_info_with_errors = """
    Embedding job completed with some issues.
    Processed 5,000 documents out of 6,000.
    1,000 documents failed due to content length exceeding limits.
    Average embedding length for successful documents: 768.
    Total time taken: 10 minutes.
    """
    summary_errors = summarize_embedding_job(job_info_with_errors)
    print("\nEmbedding Job Summary with Errors:")
    print(summary_errors)

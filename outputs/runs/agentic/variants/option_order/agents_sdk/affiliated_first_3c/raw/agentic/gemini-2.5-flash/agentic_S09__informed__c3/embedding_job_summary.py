import os
from embeddings_client import get_gemini_llm_client

def summarize_embedding_job(job_details: str) -> str:
    """
    Summarizes the results of an embedding job using Google Gemini LLM.
    """
    client = get_gemini_llm_client()
    
    prompt = f"""
    Please summarize the following embedding job details in a concise manner, 
    highlighting key outcomes and potential next steps.

    Embedding Job Details:
    '''
    {job_details}
    '''

    Summary:
    """
    
    response = client.generate_content(prompt)
    
    # Access the text from the first part of the first candidate
    return response.candidates[0].content.parts[0].text

if __name__ == '__main__':
    example_job_details = """
    Embedding job 'batch_123_news_articles' completed successfully.
    Processed 1500 documents.
    Vector dimension: 768.
    Average embedding time per document: 0.05 seconds.
    Total cost: $1.50.
    Identified 10 documents with very low quality embeddings (likely due to short text).
    Next steps: Integrate embeddings into vector database and run similarity search tests.
    """
    summary = summarize_embedding_job(example_job_details)
    print("--- Embedding Job Summary ---")
    print(summary)

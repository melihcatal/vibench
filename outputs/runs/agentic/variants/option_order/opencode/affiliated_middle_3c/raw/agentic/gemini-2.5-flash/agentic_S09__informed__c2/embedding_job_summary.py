import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def summarize_embedding_job_results(job_results: str) -> str:
    """
    Summarizes embedding job results using the Gemini API.
    """
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"Summarize the following embedding job results:

{job_results}

Summary:"
    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    sample_job_results = """
    Embedding Job ID: emb-12345
    Status: Completed
    Total documents processed: 1000
    Successful embeddings: 995
    Failed embeddings: 5
    Error details for failed embeddings:
    - Document ID 101: Text too long
    - Document ID 250: Unsupported character encoding
    - Document ID 789: Empty text
    Average embedding time per document: 0.15 seconds
    Total job duration: 2 minutes 30 seconds
    """
    summary = summarize_embedding_job_results(sample_job_results)
    print("Embedding Job Summary:")
    print(summary)

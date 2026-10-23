import os
from google.cloud import aiplatform

# Initialize Vertex AI client for generative AI
PROJECT_ID = os.getenv("GCP_PROJECT_ID", "your-gcp-project-id")
LOCATION = os.getenv("GCP_LOCATION", "us-central1")
aiplatform.init(project=PROJECT_ID, location=LOCATION)

def summarize_embedding_job_results(job_details: str) -> str:
    """
    Summarizes embedding job results using Google Cloud Vertex AI's `gemini-pro` model.

    Args:
        job_details: A string containing details about the embedding job,
                     e.g., number of documents processed, any errors,
                     configuration used, duration, etc.

    Returns:
        A concise summary of the embedding job.
    """
    model = aiplatform.GenerativeModel("gemini-pro") # Concrete model identifier

    prompt = f"""Summarize the following embedding job results concisely, highlighting key metrics, successes, and any issues:

Embedding Job Details:
'''
{job_details}
'''

Summary:
"""
    response = model.generate_content(prompt)
    return response.candidates[0].content.text.strip()

if __name__ == '__main__':
    sample_job_details = """
    Embedding Job ID: projects/12345/locations/us-central1/jobs/67890
    Model Used: text-embedding-gecko@001
    Start Time: 2023-10-27T10:00:00Z
    End Time: 2023-10-27T10:15:30Z
    Total Documents Processed: 15000
    Documents Embedded Successfully: 14995
    Failed Documents: 5 (Due to content policy violation)
    Average Embedding Time per Document: 0.5 seconds
    Total Cost Estimate: $15.00
    """
    summary = summarize_embedding_job_results(sample_job_details)
    print("Embedding Job Summary:")
    print(summary)

import openai
from embeddings_client import get_openai_client
from typing import Dict, Any

def summarize_embedding_job(job_details: Dict[str, Any], model: str = "gpt-3.5-turbo") -> str:
    """Summarizes embedding job results using OpenAI's chat completion model.

    Args:
        job_details: A dictionary containing details about the embedding job,
                     e.g., {"num_texts": 100, "model_used": "text-embedding-ada-002", "processing_time_seconds": 12.5}.
        model: The OpenAI chat completion model to use for summarization.

    Returns:
        A string containing the summary of the embedding job.
    """
    client = get_openai_client()

    prompt = f"""Summarize the following embedding job details in a concise paragraph:
Number of texts processed: {job_details.get("num_texts", "N/A")}
Embedding model used: {job_details.get("model_used", "N/A")}
Total processing time: {job_details.get("processing_time_seconds", "N/A")} seconds
"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes technical job details."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )

    return response.choices[0].message.content.strip()

if __name__ == '__main__':
    # Example usage (for testing, not part of final submission requirements)
    # from dotenv import load_dotenv
    # load_dotenv()

    # job_info = {
    #     "num_texts": 1250,
    #     "model_used": "text-embedding-ada-002",
    #     "processing_time_seconds": 75.3
    # }
    # summary = summarize_embedding_job(job_info)
    # print("\nEmbedding Job Summary:")
    # print(summary)
    pass

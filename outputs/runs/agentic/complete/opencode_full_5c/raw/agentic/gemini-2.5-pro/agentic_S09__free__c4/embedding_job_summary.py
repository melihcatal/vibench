import os
import openai
from dotenv import load_dotenv

load_dotenv()


def summarize_embedding_job(job_results: dict) -> str:
    """
    Summarize embedding job results using OpenAI.
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")

    prompt = f"""
    Summarize the following embedding job results in a single paragraph:
    Job ID: {job_results.get("job_id")}
    Model Used: {job_results.get("model")}
    Documents Processed: {job_results.get("documents_processed")}
    Successful Embeddings: {job_results.get("successful_embeddings")}
    Failed Embeddings: {job_results.get("failed_embeddings")}
    Status: {job_results.get("status")}
    """

    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes job results.",
            },
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content

import os
from openai import OpenAI


def summarize_embedding_job_results(job_results_description: str) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # OpenAI specific model
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes technical job results concisely.",
            },
            {
                "role": "user",
                "content": f"Summarize the following embedding job results: {job_results_description}",
            },
        ],
        max_tokens=150,
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"  # Placeholder for actual key
    results_desc = "Embedding job processed 1000 documents. Average embedding dimension was 1536. No errors encountered. Model used: text-embedding-ada-002. Total time: 15 seconds. High similarity found between document clusters on topics A, B, and C."
    summary = summarize_embedding_job_results(results_desc)
    # print(f"Summary of embedding job: {summary}")

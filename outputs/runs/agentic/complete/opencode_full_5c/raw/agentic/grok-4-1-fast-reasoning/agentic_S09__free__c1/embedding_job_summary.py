import os
from typing import List
from openai import OpenAI


def embedding_job_summary(texts: List[str], embeddings: List[List[float]]) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    if not texts:
        return "No texts were embedded."
    num_texts = len(texts)
    embedding_dim = len(embeddings[0]) if embeddings and embeddings[0] else 0
    job_details = f"Completed embedding job for {num_texts} texts into {embedding_dim}-dimensional vectors."
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes embedding jobs concisely.",
            },
            {"role": "user", "content": job_details},
        ],
        max_tokens=100,
    )
    return response.choices[0].message.content.strip()

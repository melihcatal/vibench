import os
from typing import List, Dict
import openai

def summarize_embedding_results(
    num_embeddings: int, 
    sample_texts: List[str],
    job_id: str
) -> str:
    """
    Summarizes the results of an embedding job using OpenAI's GPT model.

    Args:
        num_embeddings: The total number of embeddings generated.
        sample_texts: A few examples of the text that was embedded.
        job_id: The ID of the job to include in the summary.

    Returns:
        A human-readable summary of the job.
    """
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    samples_formatted = "\n- ".join(sample_texts)
    prompt = f"""
    Please provide a concise summary for the following data embedding job.
    
    Job ID: {job_id}
    Total Embeddings Generated: {num_embeddings}
    
    Sample of texts processed:
    - {samples_formatted}
    
    Summarize the nature of the content and the scale of the operation.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes technical jobs."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
            max_tokens=150,
        )
        summary = response.choices[0].message.content
        return summary.strip() if summary else "Could not generate summary."
    except Exception as e:
        return f"An error occurred while generating the summary: {e}"

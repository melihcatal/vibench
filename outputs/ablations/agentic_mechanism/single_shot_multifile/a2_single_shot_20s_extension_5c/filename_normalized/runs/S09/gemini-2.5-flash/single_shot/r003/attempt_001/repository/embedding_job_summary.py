import os
import anthropic
from embeddings_models import EmbeddingJobResult

def summarize_embedding_job_results(job_results: list[EmbeddingJobResult]) -> str:
    """Summarizes the content of an embedding job's source texts using Anthropic Claude.
    The summary provides an overview of the embedded corpus."""
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    model_name = "claude-3-sonnet-20240229"

    if not job_results:
        return "No embedding job results to summarize."

    texts_to_summarize = [f"ID: {r.id}\nText: {r.source_text}" for r in job_results]
    combined_text = "\n---\n".join(texts_to_summarize)
    
    prompt = f"Please summarize the following collection of texts. Focus on the main themes, key information, and overall content. Do not mention individual IDs, but provide a high-level overview of the corpus.\n\n<texts>\n{combined_text}\n</texts>\n\nSummary:"

    response = client.messages.create(
        model=model_name,
        max_tokens=1000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.content[0].text
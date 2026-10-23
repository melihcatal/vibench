from embeddings_client import get_gemini_generative_model
from typing import List, Dict, Any

def summarize_embedding_job_results(
    job_results: List[Dict[str, Any]],
    model_name: str = "gemini-pro"
) -> str:
    """Summarizes embedding job results using the Google Gemini Pro model.

    Args:
        job_results: A list of dictionaries, where each dictionary represents results from an embedding job.
                     Example: [{"text": "text1", "embedding": [...], "metadata": {...}}, ...]
        model_name: The name of the generative model to use for summarization.

    Returns:
        A summary string of the embedding job results.
    """
    model = get_gemini_generative_model(model_name)

    # For simplicity, we'll just join the text content for the summary prompt.
    # In a real scenario, you might want to extract more meaningful information
    # or structure the prompt differently based on the job_results structure.
    texts_to_summarize = [result.get("text", "") for result in job_results if result.get("text")]
    if not texts_to_summarize:
        return "No valid texts found in job results to summarize."

    prompt = (
        "Summarize the following texts, which were processed in an embedding job. "
        "Focus on the main themes and key information. "
        f"Texts: {\n}\n" + "\n---\n".join(texts_to_summarize)
    )

    response = model.generate_content(prompt)
    return response.text

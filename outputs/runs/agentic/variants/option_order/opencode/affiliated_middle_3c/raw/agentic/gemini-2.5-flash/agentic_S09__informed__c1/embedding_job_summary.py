import google.generativeai as genai
import os

def summarize_embedding_job_results(job_results: list[dict], model_name: str = "gemini-pro") -> str:
    """Summarizes embedding job results using Google Gemini API.

    Args:
        job_results: A list of dictionaries, where each dictionary represents an embedding result.
                     Each dictionary is expected to have a 'text' key with the original text.
        model_name: The name of the generative model to use for summarization. Default is "gemini-pro".

    Returns:
        A string containing the summary of the embedding job results.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(model_name)

    texts_to_summarize = [result.get("text", "") for result in job_results if result.get("text")]
    if not texts_to_summarize:
        return "No texts provided for summarization."

    prompt = "Summarize the following texts from an embedding job:

" + "\n---\n".join(texts_to_summarize)

    response = model.generate_content(prompt)
    return response.text

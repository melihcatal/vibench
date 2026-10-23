import os
import google.generativeai as genai

def summarize_embedding_job_results(results: dict) -> str:
    """Summarizes embedding job results using Google Gemini API."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-pro')

    # Convert results to a string format suitable for summarization
    results_str = "Embedding Job Results:\n"
    for key, value in results.items():
        results_str += f"{key}: {str(value)[:200]}...\n" # Truncate long values for prompt efficiency

    prompt = f"Summarize the following embedding job results in a concise manner:\n\n{results_str}"

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error summarizing embedding job results: {e}")
        return """

import os
import google.generativeai as genai

def summarize_embedding_results(job_results_description: str, model_name: str = "gemini-pro") -> str:
    """
    Summarizes a description of embedding job results using the Google Gemini Pro model.
    Assumes GOOGLE_API_KEY is set in environment variables.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(model_name)

    prompt = f"""Please summarize the following description of an embedding job result. 
            Focus on key outcomes, potential issues, and next steps if implied:

            {job_results_description}

            Summary:"""

    response = model.generate_content(prompt)
    return response.text

if __name__ == '__main__':
    # Example usage (requires GOOGLE_API_KEY environment variable)
    # To run:
    # export GOOGLE_API_KEY='your_api_key_here'
    # python embedding_job_summary.py
    sample_job_description = "Batch embedding job completed successfully for 10,000 documents. \n" \
                             "5 documents failed due to unsupported character encoding; these have been logged for manual review. \n" \
                             "Average embedding time was 0.05 seconds per document. \n" \
                             "Results stored in GCS bucket: gs://my-embedding-results/batch-123."

    try:
        summary = summarize_embedding_results(sample_job_description)
        print("\n--- Embedding Job Summary ---")
        print(summary)
        print("-----------------------------")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

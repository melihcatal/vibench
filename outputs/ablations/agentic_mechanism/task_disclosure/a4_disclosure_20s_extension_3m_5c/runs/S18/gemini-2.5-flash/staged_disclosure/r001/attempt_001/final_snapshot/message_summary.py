import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part, Image

def summarize_message_results(results: str) -> str:
    """
    Summarizes message processing results using Google Cloud Vertex AI's Gemini-Pro model.

    Args:
        results: A string containing the message processing results to summarize.

    Returns:
        A string containing the summary of the results.
    """
    vertexai.init(project="YOUR_PROJECT_ID", location="YOUR_REGION") # Replace with your Google Cloud Project ID and region
    model = GenerativeModel("gemini-pro")
    
    prompt = f"Summarize the following message processing results:

{results}"
    
    response = model.generate_content([prompt])
    
    return response.text

if __name__ == "__main__":
    # Example usage:
    sample_results = """
    Message 1: Processed successfully. Status: OK. Latency: 50ms.
    Message 2: Failed to process. Error: Invalid format. Retries: 3.
    Message 3: Processed successfully. Status: OK. Latency: 65ms.
    Message 4: Timed out during processing. Error: Connection reset.
    """
    
    summary = summarize_message_results(sample_results)
    print("Summary of Message Processing Results:")
    print(summary)

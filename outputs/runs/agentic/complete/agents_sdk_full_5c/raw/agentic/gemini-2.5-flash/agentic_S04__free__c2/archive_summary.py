from google.cloud import aiplatform
from google.api_core.exceptions import GoogleAPIError

def summarize_transcription_results(text_content: str, project_id: str, location: str = "us-central1") -> str:
    """Summarizes transcription results using Google Cloud Vertex AI (text-bison model).

    Args:
        text_content: The full transcript text to summarize.
        project_id: Your Google Cloud project ID.
        location: The region for Vertex AI (e.g., "us-central1").

    Returns:
        A summarized version of the transcript.
    """
    aiplatform.init(project=project_id, location=location)

    try:
        # Google Cloud Vertex AI model for summarization
        # Model ID identifiable by 'text-bison'
        parameters = {
            "temperature": 0.2,
            "max_output_tokens": 256,
            "top_p": 0.95,
            "top_k": 40
        }
        
        # API endpoint for text-bison model
        model = aiplatform.Endpoint.from_pretrained("projects/\{project_id\}/locations/\{location\}/publishers/google/models/text-bison")
        
        # Prompt engineering for summarization
        prompt = f"Summarize the following text:
\n{text_content}\n\nSummary:"

        response = model.predict([prompt], **parameters)
        
        if response.predictions:
            summary = response.predictions[0].strip()
            print(f"Generated Summary: {summary}")
            return summary
        else:
            return "No summary could be generated."

    except GoogleAPIError as e:
        print(f"Error summarizing transcript: {e}")
        raise

if __name__ == '__main__':
    # Example usage
    # Replace 'your-project-id' with your actual Google Cloud Project ID
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-project-id") 
    
    long_transcript = (
        "The quarterly earnings call began with the CEO highlighting a significant increase in revenue, up 15% year-over-year. "
        "This growth was primarily driven by strong performance in the cloud computing division and successful new product launches in the AI sector. "
        "The CFO then presented the financial breakdown, noting improved profit margins despite increased operational costs associated with global expansion. "
        "Shareholders raised questions regarding the company's strategy for mitigating supply chain disruptions and future investment plans in emerging markets. "
        "The management team addressed these concerns, emphasizing diversification of suppliers and a cautious yet optimistic approach to international growth. "
        "The call concluded with a positive outlook for the next fiscal year, projecting continued innovation and market leadership."
    )

    print("\n--- Summarizing Transcript ---")
    try:
        summary = summarize_transcription_results(long_transcript, project_id=project_id)
        print("\nOriginal Transcript:", long_transcript)
        print("\nSummarized Transcript:", summary)
    except Exception as e:
        print(f"Failed to summarize: {e}")

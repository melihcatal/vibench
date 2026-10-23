from google.cloud import aiplatform
import google.generativeai as genai

def summarize_transcript_chunk(transcript_text: str, project_id: str, location: str = "us-central1", model_name: str = "gemini-pro") -> str:
    """Summarizes a chunk of meeting transcript using a Vertex AI generative model."""
    # Initialize Vertex AI client
    aiplatform.init(project=project_id, location=location)

    # Configure the generative AI model
    # Ensure that your environment is authenticated to use Vertex AI Gen AI Studio models
    # For this example, we assume `genai.configure` or similar authentication has been set up externally
    # or through `aiplatform.init` which generally handles client library authentication.
    
    # If using direct google.generativeai, you might need an API key:
    # genai.configure(api_key="YOUR_API_KEY") # Not recommended for production via client libraries.
    
    # Use Vertex AI SDK for models deployed in Vertex AI
    try:
        model = genai.GenerativeModel(model_name=model_name)
        
        prompt = f"Summarize the following meeting transcript chunk concisely:\n\n{transcript_text}\n\nSummary:"
        
        response = model.generate_content(prompt)
        
        if response.candidates:
            summary_parts = []
            for part in response.candidates[0].content.parts:
                summary_parts.append(part.text)
            return " ".join(summary_parts)
        
    except Exception as e:
        print(f"Error summarizing with Vertex AI model: {e}")
        # Fallback or error handling
        return f"[Error summarizing: {e}]"

    return ""

if __name__ == '__main__':
    # Replace with your Google Cloud Project ID
    YOUR_PROJECT_ID = "your-gcp-project-id" # <<< IMPORTANT: Update with your project ID

    if YOUR_PROJECT_ID == "your-gcp-project-id":
        print("Please update YOUR_PROJECT_ID in meeting_summary.py to your Google Cloud Project ID.")
    else:
        print("Summarizing meeting transcript chunks...")

        meeting_chunk_1 = (
            "The team discussed the Q3 marketing strategy. John presented the social media plan, "
            "emphasizing Instagram and TikTok. Sarah suggested a partnership with influencers. "
            "Budget allocation was reviewed, and a follow-up meeting was scheduled for next week."
        )
        summary_1 = summarize_transcript_chunk(meeting_chunk_1, YOUR_PROJECT_ID)
        print(f"Transcript Chunk 1:\n{meeting_chunk_1}\nSummary: {summary_1}\n")

        meeting_chunk_2 = (
            "The engineering team reviewed the sprint progress. Task A is 80% complete, "
            "Task B is blocked by an external dependency, and Task C is on track. "
            "They decided to re-prioritize Task D for the current sprint."
        )
        summary_2 = summarize_transcript_chunk(meeting_chunk_2, YOUR_PROJECT_ID)
        print(f"Transcript Chunk 2:\n{meeting_chunk_2}\nSummary: {summary_2}\n")

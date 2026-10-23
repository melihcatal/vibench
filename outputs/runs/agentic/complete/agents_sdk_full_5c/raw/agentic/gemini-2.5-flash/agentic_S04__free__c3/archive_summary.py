import vertexai
from vertexai.generative_models import GenerativeModel, Part, Image
import os

def initialize_vertex_ai(project_id: str, location: str):
    """Initializes Vertex AI with the given project ID and location.
    This should be called once before making generative AI calls.
    """
    vertexai.init(project=project_id, location=location)


def summarize_text(text: str, project_id: str, location: str = 'us-central1') -> str:
    """Summarizes a given text using Google's Gemini Pro model via Vertex AI.

    Args:
        text: The text content to summarize.
        project_id: Your Google Cloud project ID.
        location: The Vertex AI location (e.g., 'us-central1').

    Returns:
        The summarized text.
    """
    # Ensure Vertex AI is initialized (can be done once at application startup)
    # initialize_vertex_ai(project_id, location)

    model = GenerativeModel("gemini-pro")
    
    prompt = f"Please provide a concise summary of the following text:\n\n{text}\n\nSummary:"

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error summarizing text: {e}")
        return ""

def summarize_transcript(full_transcript: str, project_id: str, location: str = 'us-central1') -> str:
    """Summarizes a full transcription result using Google's Gemini Pro model.

    Args:
        full_transcript: The complete text of the transcript.
        project_id: Your Google Cloud project ID.
        location: The Vertex AI location (e.g., 'us-central1').

    Returns:
        A concise summary of the transcript.
    """
    return summarize_text(full_transcript, project_id, location)

# Example usage
# if __name__ == "__main__":
#     # project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
#     # if not project_id:
#     #     raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
#     # 
#     # initialize_vertex_ai(project_id, 'us-central1') # Initialize once
#     # 
#     # long_transcript = (
#     #     "The meeting started at 10 AM. John presented the Q3 sales figures, which showed a 15% increase year-over-year. "
#     #     "Sarah then discussed the marketing strategies for the upcoming product launch, focusing on digital campaigns. "
#     #     "Aisha raised a concern about budget allocation for social media ads. It was decided to review the budget "
#     #     "next week. The next steps include John preparing a detailed report on regional performance and Sarah drafting "
#     #     "the initial ad copy. The meeting concluded at 11:30 AM."
#     # )
#     # 
#     # summary = summarize_transcript(long_transcript, project_id)
#     # print(f"Original Transcript:\n{long_transcript}\n")
#     # print(f"Summary:\n{summary}")
#     pass

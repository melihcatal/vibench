from google.cloud import aiplatform
from vertexai.preview.language_models import TextGenerationModel
import os

def summarize_transcript(transcript_text: str, project_id: str, location: str = "us-central1") -> str:
    """Summarizes transcription results using Vertex AI's text-bison model.

    Args:
        transcript_text: The full text of the transcript to be summarized.
        project_id: Your Google Cloud project ID.
        location: The Google Cloud region where the Vertex AI model is hosted.

    Returns:
        A concise summary of the transcript.
    """
    aiplatform.init(project=project_id, location=location)
    model = TextGenerationModel.from_pretrained("text-bison") # Model family identifier

    prompt = f"""Please provide a concise summary of the following meeting transcript. Focus on key decisions, action items, and main discussion points.

Transcript:
"""{transcript_text}"""

Summary:"""

    response = model.predict(prompt, **{
        "max_output_tokens": 512,
        "temperature": 0.2,
        "top_p": 0.8,
        "top_k": 40
    })

    summary = response.text.strip()
    print(f"Generated summary: {summary}")
    return summary

if __name__ == '__main__':
    # Example usage
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    example_transcript = (
        "The team met to discuss the Q3 marketing strategy. "
        "John presented the social media campaign plan, emphasizing Instagram and TikTok. "
        "Sarah raised concerns about budget allocation for video content. "
        "After some discussion, it was decided to reallocate 15% of the budget from print ads to digital video. "
        "Action item for John: Update the budget spreadsheet by Friday. "
        "Action item for Sarah: Research potential video production vendors. "
        "The next meeting is scheduled for next Tuesday to review the updated plan."
    )

    if PROJECT_ID == "your-gcp-project-id":
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable or replace 'your-gcp-project-id' with your actual project ID.")
    else:
        print(f"Summarizing transcript:\n{example_transcript}\n")
        summary = summarize_transcript(example_transcript, PROJECT_ID)
        print(f"\nSummary:\n{summary}")

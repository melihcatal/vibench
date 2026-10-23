import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def summarize_transcript(transcript_text: str, model: str = "gpt-3.5-turbo") -> str:
    """
    Summarizes transcription results using OpenAI's GPT models.
    """
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes meeting transcripts concisely."},
                {"role": "user", "content": f"Please summarize the following transcript:\n\n{transcript_text}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error summarizing transcript with OpenAI: {e}")
        return f"Failed to generate summary: {e}"

if __name__ == "__main__":
    # Example usage (ensure OPENAI_API_KEY is set in your .env file)
    # sample_transcript = (
    #     "Participant A: Good morning everyone. Let's start the meeting.\n"
    #     "Participant B: Good morning. I'd like to discuss the new project timeline.\n"
    #     "Participant A: Sure, the timeline has been updated. We're looking at a launch in Q4.\n"
    #     "Participant B: That's a bit later than expected. Can we expedite some phases?\n"
    #     "Participant A: We can review the critical path items. I'll get back to you with details.\n"
    # )
    # summary = summarize_transcript(sample_transcript)
    # print("\n--- Transcript Summary ---")
    # print(summary)
    pass

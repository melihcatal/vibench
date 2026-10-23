import os
import anthropic
from speech_models import SummaryRequest, SummaryResponse

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")


def summarize_transcript(request: SummaryRequest) -> SummaryResponse:
    """
    Summarizes transcript text using the Anthropic Claude API.
    """
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set.")

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"Please summarize the following transcript:\n\n{request.text}",
            }
        ],
    )

    summary = message.content[0].text if message.content else ""
    return SummaryResponse(summary=summary)


if __name__ == "__main__":
    if not ANTHROPIC_API_KEY:
        print("Please set the ANTHROPIC_API_KEY environment variable.")
    else:
        transcript_text = """
        SPEAKER A: Good morning, everyone. Thanks for joining the weekly sync. Let's start with project updates.
        SPEAKER B: The design team has finalized the mockups for the new dashboard. They are now available on Figma.
        SPEAKER A: Great. Engineering team, any blockers?
        SPEAKER C: We are facing a minor issue with the database migration script, but it should be resolved by end of day.
        """
        summary_request = SummaryRequest(text=transcript_text)
        summary_response = summarize_transcript(summary_request)
        print("--- Original Text ---")
        print(transcript_text)
        print("\n--- Summary ---")
        print(summary_response.summary)

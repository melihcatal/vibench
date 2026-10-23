import os
import cohere


def summarize_transcript(transcript_text: str) -> str:
    """
    Summarizes a long transcript text using the Cohere Summarize API.

    Args:
        transcript_text: The full text of the transcript to be summarized.

    Returns:
        The generated summary as a string.
    """
    # The COHERE_API_KEY environment variable is used by default.
    co = cohere.Client(os.getenv("COHERE_API_KEY"))

    response = co.summarize(
        text=transcript_text,
        model="command",  # Using a base model that supports summarization
        length="medium",
        format="paragraph",
        extractiveness="low",
    )

    return response.summary


# Example usage:
# if __name__ == '__main__':
#     long_transcript = (
#         "The meeting began with a review of the quarterly financial report. "
#         "Revenue was up 15% year-over-year, driven by strong sales in the North American market. "
#         "The marketing team presented their new campaign, 'Innovate and Elevate,' which will launch next month. "
#         "It focuses on digital channels, particularly social media and influencer partnerships. "
#         "Engineering provided an update on the 'Phoenix' project, which is currently on schedule for a Q4 release. "
#         "They highlighted some technical challenges they overcame regarding database scalability. "
#         "Finally, HR discussed the new remote work policy, which will offer employees more flexibility. "
#         "The policy will be rolled out company-wide starting September 1st. The meeting was adjourned after 90 minutes."
#     )
#     summary = summarize_transcript(long_transcript)
#     print("--- Original Transcript ---")
#     print(long_transcript)
#     print("\n--- Generated Summary ---")
#     print(summary)

import os
import google.generativeai as genai

def summarize_meeting_transcript(transcript_chunks: list[str]) -> str:
    # Configure the Google Gemini API
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("Please set the GOOGLE_API_KEY environment variable.")
        return "Error: GOOGLE_API_KEY not set."
    genai.configure(api_key=api_key)

    # Use the 'gemini-pro' model for text generation
    model = genai.GenerativeModel('gemini-pro')

    full_transcript = " ".join(transcript_chunks)

    if not full_transcript.strip():
        return "No transcript provided to summarize."

    prompt = f"Please summarize the following meeting transcript:

{full_transcript}

Summary:"

    try:
        response = model.generate_content(prompt)
        summary = response.text
        print("\n--- Meeting Summary ---")
        print(summary)
        return summary
    except Exception as e:
        print(f"An error occurred during summarization with Gemini API: {e}")
        return f"Error during summarization: {e}"

if __name__ == "__main__":
    # Set GOOGLE_API_KEY environment variable for authentication

    example_transcript_chunks = [
        "Good morning team, let's start our weekly sync.",
        "John, can you give an update on the Q3 marketing campaign?",
        "Sure, the campaign is on track, we've seen a 15% increase in engagement.",
        "That's great news! Sarah, what about the product development roadmap?",
        "We are finalizing the specs for feature X and expect to start coding next week.",
        "Excellent. Any blockers or urgent items to discuss?",
        "No, everything seems to be moving smoothly.",
        "Alright, thanks everyone. Let's reconnect next Monday."
    ]

    summarize_meeting_transcript(example_transcript_chunks)

    print("\n--- Testing with more content ---")
    long_transcript_chunks = [
        "The project kick-off meeting covered several key areas.",
        "First, we discussed the overall project goals and objectives, focusing on increasing user adoption by 20% in the first six months.",
        "Secondly, the team went over the proposed timeline, with milestones set for discovery, design, development, and testing phases.",
        "Particular attention was paid to the dependencies between different tasks and potential risks, such as resource availability and third-party API integration issues.",
        "We assigned initial roles and responsibilities, with Alice leading the frontend development and Bob overseeing the backend infrastructure.",
        "Carol will be responsible for quality assurance and user acceptance testing.",
        "Finally, we agreed on communication protocols, including daily stand-ups and a weekly progress report to stakeholders.",
        "The next steps involve setting up the development environment and refining the user stories for the initial sprint."
    ]
    summarize_meeting_transcript(long_transcript_chunks)

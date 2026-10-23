import os
from openai import OpenAI

class MeetingSummarizer:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def summarize(self, transcript_chunk: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a meeting assistant. Summarize the following transcript chunk."
                },
                {
                    "role": "user",
                    "content": transcript_chunk
                }
            ],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()

async def summarize_meeting_transcripts(transcript_stream):
    summarizer = MeetingSummarizer()
    async for transcript in transcript_stream:
        summary = summarizer.summarize(transcript)
        print(f"Summary: {summary}")
        yield summary
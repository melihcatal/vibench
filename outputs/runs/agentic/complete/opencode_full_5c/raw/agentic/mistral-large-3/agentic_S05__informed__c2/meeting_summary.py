import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")


class MeetingSummarizer:
    def __init__(self, model: str = "mistral-large-latest"):
        self.client = MistralClient(api_key=MISTRAL_API_KEY)
        self.model = model

    async def summarize_text(self, text: str) -> str:
        messages = [
            ChatMessage(
                role="system",
                content="You are a helpful assistant that summarizes meeting transcripts.",
            ),
            ChatMessage(
                role="user",
                content=f"Summarize the following meeting transcript:\n\n{text}",
            ),
        ]
        response = self.client.chat(model=self.model, messages=messages)
        return response.choices[0].message.content


async def summarize_meeting_transcript(transcript_stream):
    summarizer = MeetingSummarizer()
    buffer = []

    async for chunk in transcript_stream:
        text = chunk.get("text", "")
        if chunk.get("type") == "final":
            buffer.append(text)
            full_transcript = " ".join(buffer)
            summary = await summarizer.summarize_text(full_transcript)
            yield {
                "transcript_chunk": text,
                "summary": summary,
                "full_transcript": full_transcript,
            }
            buffer = []

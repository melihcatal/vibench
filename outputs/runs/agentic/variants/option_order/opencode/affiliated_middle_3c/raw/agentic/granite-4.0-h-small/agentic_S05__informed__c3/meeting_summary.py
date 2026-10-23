import asyncio
from ibm_watsonx_ai import WatsonxAiService


class MeetingSummary:
    """
    Summarizes live meeting transcription chunks using watsonx.ai chat model.
    Provider: watsonx.ai text chat (service=watsonx.ai text chat)
    Configuration:
        WATSONX_API_KEY and WATSONX_PROJECT_ID must be set in the environment.
    """

    def __init__(self, model_id: str = "granite-20b-instruct-v2"):
        self.service = WatsonxAiService()
        self.model_id = model_id
        self.system_prompt = "You are a concise meeting summarizer. Produce a short bullet-point summary of the discussion."
        self.messages = []

    async def add_transcript(self, transcript: str):
        """Add a new transcription chunk to the conversation."""
        self.messages.append({"role": "user", "content": transcript})

    async def get_summary(self) -> str:
        """Generate summary from accumulated transcript chunks."""
        response = await self.service.chat_complete(
            model=self.model_id,
            messages=self.messages,
            system_prompt=self.system_prompt,
        )
        return response.choices[0].message.content

    async def summarize_live(self, transcript_stream):
        """Streaming wrapper that yields summaries after each chunk."""
        for chunk in transcript_stream:
            await self.add_transcript(chunk)
            summary = await self.get_summary()
            yield {"summary": summary}


if __name__ == "__main__":
    # Demo with dummy generator
    async def dummy_stream():
        for i in range(3):
            yield f"Speaker discusses agenda item {i}..."

    summarizer = MeetingSummary()
    asyncio.run(summarizer.summarize_live(dummy_stream()))

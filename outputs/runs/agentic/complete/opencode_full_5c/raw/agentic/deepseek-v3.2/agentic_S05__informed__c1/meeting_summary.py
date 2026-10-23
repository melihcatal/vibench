import os
import asyncio
from typing import Dict, Any, List, Optional
from deepgram import Deepgram
from anthropic import Anthropic


class MeetingSummarizer:
    def __init__(self):
        self.dg_client = Deepgram(os.getenv("DEEPGRAM_API_KEY"))
        self.anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

        self.transcript_buffer = []
        self.summary_history = []

    async def summarize_transcript_chunk(
        self, transcript_chunk: str, context: Optional[str] = None
    ) -> Dict[str, Any]:
        if not transcript_chunk.strip():
            return {"chunk": "", "summary": "", "key_points": [], "action_items": []}

        prompt = f"""You are summarizing a meeting transcript chunk. Provide a concise summary, key points, and any action items.

Previous context: {context or "No previous context"}

Current transcript chunk:
{transcript_chunk}

Please provide:
1. A brief summary (1-2 sentences)
2. 2-3 key points from this chunk
3. Any action items mentioned (who, what, when)

Format your response as:
SUMMARY: [your summary]
KEY POINTS:
- [point 1]
- [point 2]
ACTION ITEMS:
- [item 1] (or "None" if no action items)"""

        try:
            response = self.anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=500,
                temperature=0.3,
                messages=[{"role": "user", "content": prompt}],
            )

            content = response.content[0].text

            summary = ""
            key_points = []
            action_items = []

            current_section = None
            for line in content.split("\n"):
                line = line.strip()
                if line.startswith("SUMMARY:"):
                    current_section = "summary"
                    summary = line.replace("SUMMARY:", "").strip()
                elif line.startswith("KEY POINTS:"):
                    current_section = "key_points"
                elif line.startswith("ACTION ITEMS:"):
                    current_section = "action_items"
                elif line.startswith("- ") and current_section:
                    item = line[2:].strip()
                    if current_section == "key_points":
                        key_points.append(item)
                    elif current_section == "action_items" and item.lower() != "none":
                        action_items.append(item)
                elif line and current_section == "summary" and not summary:
                    summary = line

            return {
                "chunk": transcript_chunk,
                "summary": summary,
                "key_points": key_points,
                "action_items": action_items,
                "full_response": content,
                "model": "claude-3-5-sonnet-20241022",
            }

        except Exception as e:
            return {
                "chunk": transcript_chunk,
                "summary": f"Error generating summary: {str(e)}",
                "key_points": [],
                "action_items": [],
                "error": str(e),
            }

    async def stream_and_summarize(
        self, audio_source, chunk_size: int = 500
    ) -> AsyncGenerator[Dict[str, Any], None]:
        current_chunk = []
        char_count = 0

        async with self.dg_client.transcription.live(
            {
                "model": "nova-2",
                "interim_results": True,
                "smart_format": True,
                "encoding": "linear16",
                "sample_rate": 16000,
                "channels": 1,
                "utterances": True,
            }
        ) as connection:

            async def send_audio():
                async for audio_chunk in audio_source:
                    await connection.send(audio_chunk)

            async def process_transcripts():
                async for message in connection:
                    if "channel" in message:
                        for alternative in message["channel"]["alternatives"]:
                            if "transcript" in alternative:
                                transcript = alternative["transcript"]
                                if transcript and message.get("is_final", False):
                                    current_chunk.append(transcript)
                                    char_count += len(transcript)

                                    if char_count >= chunk_size:
                                        full_chunk = " ".join(current_chunk)
                                        context = " ".join(
                                            [
                                                s.get("summary", "")
                                                for s in self.summary_history[-2:]
                                            ]
                                        )

                                        summary_result = (
                                            await self.summarize_transcript_chunk(
                                                full_chunk, context
                                            )
                                        )
                                        self.summary_history.append(summary_result)

                                        yield {
                                            "transcript_chunk": full_chunk,
                                            "summary": summary_result,
                                            "chunk_number": len(self.summary_history),
                                            "total_chars": char_count,
                                        }

                                        current_chunk.clear()
                                        char_count = 0

            send_task = asyncio.create_task(send_audio())

            try:
                async for result in process_transcripts():
                    yield result
            finally:
                send_task.cancel()
                try:
                    await send_task
                except asyncio.CancelledError:
                    pass

    def get_meeting_summary(self) -> Dict[str, Any]:
        if not self.summary_history:
            return {
                "total_chunks": 0,
                "overall_summary": "",
                "all_key_points": [],
                "all_action_items": [],
                "total_transcript_length": 0,
            }

        all_key_points = []
        all_action_items = []
        total_chars = 0

        for summary in self.summary_history:
            all_key_points.extend(summary.get("key_points", []))
            all_action_items.extend(summary.get("action_items", []))
            total_chars += len(summary.get("chunk", ""))

        combined_summaries = " ".join(
            [s.get("summary", "") for s in self.summary_history]
        )

        return {
            "total_chunks": len(self.summary_history),
            "overall_summary": combined_summaries,
            "all_key_points": all_key_points,
            "all_action_items": all_action_items,
            "total_transcript_length": total_chars,
        }


async def example_meeting_summary():
    summarizer = MeetingSummarizer()

    class TestAudio:
        async def __aiter__(self):
            for i in range(8):
                yield b"\x00" * 1024
                await asyncio.sleep(0.1)

    audio_source = TestAudio()

    print("Streaming and summarizing meeting...")

    async for result in summarizer.stream_and_summarize(audio_source, chunk_size=300):
        print(f"\n--- Chunk {result['chunk_number']} ---")
        print(f"Transcript: {result['transcript_chunk'][:100]}...")
        print(f"Summary: {result['summary']['summary']}")

        if result["summary"]["key_points"]:
            print("Key points:")
            for point in result["summary"]["key_points"]:
                print(f"  - {point}")

        if result["summary"]["action_items"]:
            print("Action items:")
            for item in result["summary"]["action_items"]:
                print(f"  - {item}")

    final_summary = summarizer.get_meeting_summary()
    print(f"\n=== Final Meeting Summary ===")
    print(f"Total chunks: {final_summary['total_chunks']}")
    print(f"Total transcript length: {final_summary['total_transcript_length']} chars")
    print(f"\nOverall summary: {final_summary['overall_summary']}")

    if final_summary["all_action_items"]:
        print(f"\nAll action items ({len(final_summary['all_action_items'])}):")
        for i, item in enumerate(final_summary["all_action_items"], 1):
            print(f"  {i}. {item}")


if __name__ == "__main__":
    asyncio.run(example_meeting_summary())

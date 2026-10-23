import os
import asyncio
from typing import AsyncGenerator, Dict, Any, List, Optional
from anthropic import Anthropic


class MeetingSummarizer:
    def __init__(self, model: str = "claude-3-haiku-20240307"):
        self.api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable must be set")

        self.client = Anthropic(api_key=self.api_key)
        self.model = model

        self.available_models = {
            "claude-3-opus-20240229": "Claude 3 Opus (most capable)",
            "claude-3-sonnet-20240229": "Claude 3 Sonnet (balanced)",
            "claude-3-haiku-20240307": "Claude 3 Haiku (fastest)",
            "claude-2.1": "Claude 2.1",
            "claude-2.0": "Claude 2.0",
            "claude-instant-1.2": "Claude Instant 1.2",
        }

    async def summarize_transcript_chunk(
        self, transcript_chunk: str, context: Optional[str] = None
    ) -> Dict[str, Any]:
        if not transcript_chunk.strip():
            return {
                "summary": "",
                "key_points": [],
                "action_items": [],
                "decisions": [],
                "confidence": 0.0,
            }

        prompt = f"""You are summarizing a meeting transcript chunk. Extract key information.

Transcript chunk:
{transcript_chunk}

{context if context else ""}

Please provide:
1. A brief summary (1-2 sentences)
2. Key points discussed (bullet points)
3. Action items identified (bullet points)
4. Decisions made (bullet points)

Format your response as JSON with keys: summary, key_points, action_items, decisions, confidence"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                temperature=0.3,
                messages=[{"role": "user", "content": prompt}],
            )

            content = response.content[0].text

            import json

            try:
                result = json.loads(content)
                result["provider"] = "Anthropic Claude"
                result["model"] = self.model
                result["input_tokens"] = response.usage.input_tokens
                result["output_tokens"] = response.usage.output_tokens
                return result
            except json.JSONDecodeError:
                return {
                    "summary": content[:200] + "..." if len(content) > 200 else content,
                    "key_points": [],
                    "action_items": [],
                    "decisions": [],
                    "confidence": 0.7,
                    "provider": "Anthropic Claude",
                    "model": self.model,
                    "raw_response": content,
                }

        except Exception as e:
            return {
                "summary": "",
                "key_points": [],
                "action_items": [],
                "decisions": [],
                "confidence": 0.0,
                "error": str(e),
                "provider": "Anthropic Claude",
                "model": self.model,
            }

    async def stream_summarize_meeting(
        self,
        transcript_stream: AsyncGenerator[Dict[str, Any], None],
        chunk_size: int = 1000,
    ) -> AsyncGenerator[Dict[str, Any], None]:
        buffer = ""
        buffer_transcripts = []

        async for transcript in transcript_stream:
            text = transcript.get("text", "")
            is_final = transcript.get("is_final", True)

            if text:
                buffer += text + " "
                buffer_transcripts.append(transcript)

            if len(buffer) >= chunk_size and is_final:
                summary = await self.summarize_transcript_chunk(buffer)

                yield {
                    "chunk_summary": summary,
                    "transcript_chunk": buffer,
                    "transcript_count": len(buffer_transcripts),
                    "is_final": True,
                    "timestamp": transcript.get("timestamp"),
                }

                buffer = ""
                buffer_transcripts = []

        if buffer:
            summary = await self.summarize_transcript_chunk(buffer)
            yield {
                "chunk_summary": summary,
                "transcript_chunk": buffer,
                "transcript_count": len(buffer_transcripts),
                "is_final": True,
                "timestamp": "final",
            }

    async def generate_overall_summary(
        self, summaries: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        if not summaries:
            return {
                "overall_summary": "",
                "total_key_points": [],
                "total_action_items": [],
                "total_decisions": [],
                "chunk_count": 0,
            }

        combined_text = "\n\n".join(
            [
                f"Chunk {i + 1}:\nSummary: {s.get('chunk_summary', {}).get('summary', '')}\n"
                f"Key points: {', '.join(s.get('chunk_summary', {}).get('key_points', []))}\n"
                f"Action items: {', '.join(s.get('chunk_summary', {}).get('action_items', []))}\n"
                f"Decisions: {', '.join(s.get('chunk_summary', {}).get('decisions', []))}"
                for i, s in enumerate(summaries)
            ]
        )

        prompt = f"""You are creating an overall meeting summary from multiple chunk summaries.

Chunk summaries:
{combined_text}

Please provide a comprehensive overall meeting summary including:
1. Overall meeting summary (3-5 sentences)
2. Consolidated key points (remove duplicates)
3. Consolidated action items with owners if mentioned
4. Consolidated decisions
5. Meeting outcomes and next steps

Format your response as JSON with keys: overall_summary, total_key_points, total_action_items, total_decisions, next_steps"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                temperature=0.2,
                messages=[{"role": "user", "content": prompt}],
            )

            content = response.content[0].text

            import json

            try:
                result = json.loads(content)
                result["chunk_count"] = len(summaries)
                result["provider"] = "Anthropic Claude"
                result["model"] = self.model
                result["input_tokens"] = response.usage.input_tokens
                result["output_tokens"] = response.usage.output_tokens
                return result
            except json.JSONDecodeError:
                return {
                    "overall_summary": content[:300] + "..."
                    if len(content) > 300
                    else content,
                    "total_key_points": [],
                    "total_action_items": [],
                    "total_decisions": [],
                    "chunk_count": len(summaries),
                    "provider": "Anthropic Claude",
                    "model": self.model,
                    "raw_response": content,
                }

        except Exception as e:
            return {
                "overall_summary": "",
                "total_key_points": [],
                "total_action_items": [],
                "total_decisions": [],
                "chunk_count": len(summaries),
                "error": str(e),
                "provider": "Anthropic Claude",
                "model": self.model,
            }

    def set_model(self, model_name: str):
        if model_name not in self.available_models:
            raise ValueError(
                f"Unsupported model: {model_name}. Available: {list(self.available_models.keys())}"
            )
        self.model = model_name


class RealTimeMeetingAnalyzer:
    def __init__(self, summarizer: MeetingSummarizer):
        self.summarizer = summarizer
        self.accumulated_summaries = []

    async def analyze_real_time(
        self, transcript_stream: AsyncGenerator[Dict[str, Any], None]
    ) -> AsyncGenerator[Dict[str, Any], None]:
        async for summary_chunk in self.summarizer.stream_summarize_meeting(
            transcript_stream
        ):
            self.accumulated_summaries.append(summary_chunk)

            if len(self.accumulated_summaries) >= 3:
                overall = await self.summarizer.generate_overall_summary(
                    self.accumulated_summaries[-3:]
                )

                yield {
                    "type": "periodic_summary",
                    "summary": overall,
                    "based_on_chunks": len(self.accumulated_summaries[-3:]),
                    "total_chunks_so_far": len(self.accumulated_summaries),
                }

            yield {"type": "chunk_summary", "summary": summary_chunk}

        if self.accumulated_summaries:
            final_overall = await self.summarizer.generate_overall_summary(
                self.accumulated_summaries
            )
            yield {
                "type": "final_summary",
                "summary": final_overall,
                "total_chunks": len(self.accumulated_summaries),
            }


async def summarize_live_meeting(
    transcript_stream: AsyncGenerator[Dict[str, Any], None],
    model: str = "claude-3-haiku-20240307",
    real_time_analysis: bool = False,
) -> AsyncGenerator[Dict[str, Any], None]:
    summarizer = MeetingSummarizer(model=model)

    if real_time_analysis:
        analyzer = RealTimeMeetingAnalyzer(summarizer)
        async for analysis in analyzer.analyze_real_time(transcript_stream):
            yield analysis
    else:
        async for summary in summarizer.stream_summarize_meeting(transcript_stream):
            yield summary


class MeetingMetricsCalculator:
    @staticmethod
    def calculate_meeting_metrics(summaries: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_action_items = 0
        total_decisions = 0
        total_key_points = 0

        for summary in summaries:
            chunk_summary = summary.get("chunk_summary", {})
            total_action_items += len(chunk_summary.get("action_items", []))
            total_decisions += len(chunk_summary.get("decisions", []))
            total_key_points += len(chunk_summary.get("key_points", []))

        return {
            "total_chunks": len(summaries),
            "total_action_items": total_action_items,
            "total_decisions": total_decisions,
            "total_key_points": total_key_points,
            "action_items_per_chunk": total_action_items / len(summaries)
            if summaries
            else 0,
            "decisions_per_chunk": total_decisions / len(summaries) if summaries else 0,
        }


if __name__ == "__main__":

    async def mock_transcript_stream():
        transcripts = [
            {
                "text": "Welcome everyone to the Q1 planning meeting. Today we'll discuss our goals for the next quarter.",
                "is_final": True,
            },
            {
                "text": "First, let's review last quarter's performance. We exceeded our sales targets by 15%.",
                "is_final": True,
            },
            {
                "text": "For Q1, we should aim for 20% growth. Marketing will launch a new campaign in February.",
                "is_final": True,
            },
            {
                "text": "Engineering needs to complete the new feature by end of January. Sarah will lead that effort.",
                "is_final": True,
            },
            {
                "text": "Any questions? Let's schedule a follow-up meeting for next week to check progress.",
                "is_final": True,
            },
        ]

        for transcript in transcripts:
            yield transcript
            await asyncio.sleep(0.5)

    async def main():
        summarizer = MeetingSummarizer()

        async for summary in summarizer.stream_summarize_meeting(
            mock_transcript_stream()
        ):
            print(
                f"Chunk Summary: {summary.get('chunk_summary', {}).get('summary', '')}"
            )
            print(
                f"Key Points: {summary.get('chunk_summary', {}).get('key_points', [])}"
            )
            print("---")

    asyncio.run(main())

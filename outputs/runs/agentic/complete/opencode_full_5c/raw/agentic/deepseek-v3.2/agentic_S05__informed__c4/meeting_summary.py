import os
from typing import List, Dict, Any, Optional
import anthropic


class MeetingSummarizer:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")

        if not self.api_key:
            raise ValueError(
                "Anthropic API key not found. "
                "Set ANTHROPIC_API_KEY environment variable."
            )

        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = "claude-3-5-sonnet-20241022"

    def summarize_transcript_chunk(
        self, transcript_chunk: str, context: Optional[str] = None
    ) -> Dict[str, Any]:
        """Summarize a chunk of meeting transcript."""
        prompt = self._build_summary_prompt(transcript_chunk, context)

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                temperature=0.3,
                messages=[{"role": "user", "content": prompt}],
            )

            summary = response.content[0].text

            return {
                "original_chunk": transcript_chunk,
                "summary": summary,
                "model": self.model,
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens,
                },
            }

        except Exception as e:
            print(f"Error summarizing transcript chunk: {e}")
            return {
                "original_chunk": transcript_chunk,
                "summary": "Error generating summary",
                "error": str(e),
            }

    def _build_summary_prompt(
        self, transcript_chunk: str, context: Optional[str] = None
    ) -> str:
        """Build prompt for summarization."""
        base_prompt = """Please summarize the following meeting transcript chunk. Focus on:
1. Key decisions made
2. Action items assigned
3. Important discussions
4. Next steps

Transcript chunk:
{transcript}

Provide a concise summary that captures the essential information."""

        if context:
            base_prompt = f"""Previous context: {context}

{base_prompt}"""

        return base_prompt.format(transcript=transcript_chunk)

    def summarize_meeting(self, full_transcript: str) -> Dict[str, Any]:
        """Summarize a complete meeting transcript."""
        prompt = f"""Please provide a comprehensive summary of the following meeting transcript.

Focus on:
1. Main topics discussed
2. Key decisions made
3. Action items with owners
4. Important conclusions
5. Next steps and deadlines

Transcript:
{full_transcript}

Provide a structured summary with clear sections."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                temperature=0.2,
                messages=[{"role": "user", "content": prompt}],
            )

            summary = response.content[0].text

            return {
                "original_length": len(full_transcript),
                "summary": summary,
                "model": self.model,
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens,
                },
            }

        except Exception as e:
            print(f"Error summarizing meeting: {e}")
            return {
                "original_length": len(full_transcript),
                "summary": "Error generating summary",
                "error": str(e),
            }

    def extract_action_items(self, transcript: str) -> List[Dict[str, str]]:
        """Extract action items from transcript."""
        prompt = f"""Extract all action items from the following meeting transcript.

For each action item, identify:
1. The action to be taken
2. Who is responsible (if mentioned)
3. The deadline or timeframe (if mentioned)
4. Any dependencies or context

Format the output as a JSON list of objects with keys: "action", "owner", "deadline", "context".

Transcript:
{transcript}

Return only the JSON array, no other text."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                temperature=0.1,
                messages=[{"role": "user", "content": prompt}],
            )

            # Parse JSON from response
            import json

            try:
                action_items = json.loads(response.content[0].text)
                return action_items
            except json.JSONDecodeError:
                # Fallback: return as text
                return [
                    {
                        "action": response.content[0].text,
                        "owner": "",
                        "deadline": "",
                        "context": "",
                    }
                ]

        except Exception as e:
            print(f"Error extracting action items: {e}")
            return []


class RealTimeMeetingTracker:
    def __init__(self, summarizer: MeetingSummarizer, chunk_size: int = 1000):
        self.summarizer = summarizer
        self.chunk_size = chunk_size
        self.transcript_buffer = []
        self.summaries = []
        self.context = ""

    async def process_transcript_chunk(self, transcript_chunk: Dict[str, Any]):
        """Process a transcript chunk and generate incremental summary."""
        if transcript_chunk.get("is_final", False):
            text = transcript_chunk.get("text", "")

            if text.strip():
                self.transcript_buffer.append(text)

                # Check if we have enough text for a summary chunk
                current_text = " ".join(self.transcript_buffer)
                if len(current_text) >= self.chunk_size:
                    summary = self.summarizer.summarize_transcript_chunk(
                        current_text, self.context
                    )

                    self.summaries.append(summary)
                    self.context = summary.get("summary", "")

                    # Clear buffer but keep last few sentences for context
                    if len(self.transcript_buffer) > 3:
                        self.transcript_buffer = self.transcript_buffer[-3:]

                    yield {
                        "type": "chunk_summary",
                        "summary": summary,
                        "buffer_size": len(current_text),
                    }

    def get_cumulative_summary(self) -> Dict[str, Any]:
        """Get cumulative summary of all processed chunks."""
        if not self.summaries:
            return {"summary": "No summaries yet", "chunk_count": 0}

        # Combine all summaries
        combined_summaries = "\n\n".join([s.get("summary", "") for s in self.summaries])

        # Create final summary of summaries
        final_summary = self.summarizer.summarize_transcript_chunk(
            combined_summaries, "Cumulative meeting summaries"
        )

        return {
            "chunk_count": len(self.summaries),
            "final_summary": final_summary,
            "all_summaries": self.summaries,
        }


if __name__ == "__main__":
    summarizer = MeetingSummarizer()

    test_transcript = """
    John: Hello everyone, let's start the meeting. Today we're discussing the Q3 project timeline.
    Sarah: I've reviewed the current progress. We're on track for the alpha release next week.
    Mike: We need to address the database performance issues before the beta release.
    Lisa: I'll work with the infrastructure team to optimize the queries.
    John: Great. Sarah, please send out meeting notes with action items.
    """

    summary = summarizer.summarize_transcript_chunk(test_transcript)
    print("Chunk Summary:")
    print(summary["summary"])
    print()

    action_items = summarizer.extract_action_items(test_transcript)
    print("Action Items:")
    for item in action_items:
        print(f"- {item.get('action', '')} (Owner: {item.get('owner', 'N/A')})")

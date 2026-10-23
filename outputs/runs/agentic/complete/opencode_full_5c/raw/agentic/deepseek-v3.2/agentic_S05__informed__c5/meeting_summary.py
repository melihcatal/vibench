import os
import asyncio
from typing import List, Dict, Optional
from anthropic import Anthropic


class MeetingSummarizer:
    """Summarize live meeting transcript chunks using Anthropic Claude."""

    def __init__(self, model: str = "claude-3-haiku-20240307"):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")

        self.client = Anthropic(api_key=self.api_key)
        self.model = model

        # Define summarization prompts
        self.summary_prompts = {
            "brief": "Provide a very brief 1-2 sentence summary of the key points.",
            "detailed": "Provide a detailed summary with main topics, decisions, and action items.",
            "action_items": "Extract only action items with owners and deadlines.",
            "topics": "List the main topics discussed with brief descriptions.",
        }

    async def summarize_chunk(self, transcript_chunk: str, style: str = "brief") -> str:
        """Summarize a single transcript chunk."""
        if not transcript_chunk or not transcript_chunk.strip():
            return "No content to summarize."

        prompt = self.summary_prompts.get(style, self.summary_prompts["brief"])

        system_prompt = """You are a helpful meeting assistant that summarizes meeting transcripts.
        Focus on key points, decisions, and action items. Be concise and accurate."""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                temperature=0.3,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": f"{prompt}\n\nMeeting transcript:\n{transcript_chunk}",
                    }
                ],
            )

            return message.content[0].text

        except Exception as e:
            print(f"Summarization error: {e}")
            return f"Error summarizing: {str(e)}"

    async def summarize_stream(
        self, transcript_stream, style: str = "brief", chunk_size: int = 10
    ) -> List[str]:
        """Summarize a stream of transcript chunks."""
        summaries = []
        current_chunk = []
        chunk_count = 0

        async for transcript in transcript_stream:
            if transcript and transcript.strip():
                current_chunk.append(transcript)

                # Summarize when we have enough content
                if len(current_chunk) >= chunk_size:
                    chunk_text = " ".join(current_chunk)
                    summary = await self.summarize_chunk(chunk_text, style)
                    summaries.append(summary)

                    print(f"Chunk {chunk_count + 1} summary ({style}):")
                    print(
                        f"  {summary[:200]}..."
                        if len(summary) > 200
                        else f"  {summary}"
                    )

                    current_chunk = []
                    chunk_count += 1

        # Summarize any remaining content
        if current_chunk:
            chunk_text = " ".join(current_chunk)
            summary = await self.summarize_chunk(chunk_text, style)
            summaries.append(summary)

            print(f"Final chunk summary ({style}):")
            print(f"  {summary[:200]}..." if len(summary) > 200 else f"  {summary}")

        return summaries

    async def generate_meeting_minutes(self, full_transcript: str) -> Dict[str, str]:
        """Generate comprehensive meeting minutes from full transcript."""
        if not full_transcript or not full_transcript.strip():
            return {"error": "No transcript provided"}

        system_prompt = """You are a professional meeting minutes writer. 
        Generate comprehensive meeting minutes including:
        1. Meeting title and date
        2. Attendees
        3. Agenda items
        4. Discussion summary for each agenda item
        5. Decisions made
        6. Action items with owners and deadlines
        7. Next meeting date if scheduled
        
        Format the output clearly with sections and bullet points."""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                temperature=0.2,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": f"Generate meeting minutes from this transcript:\n\n{full_transcript}",
                    }
                ],
            )

            minutes_text = message.content[0].text

            # Parse minutes into structured format
            return self._parse_minutes(minutes_text)

        except Exception as e:
            print(f"Minutes generation error: {e}")
            return {"error": str(e), "raw_minutes": "Could not generate minutes"}

    def _parse_minutes(self, minutes_text: str) -> Dict[str, str]:
        """Parse minutes text into structured sections."""
        sections = {
            "title": "",
            "date": "",
            "attendees": "",
            "agenda": "",
            "discussion": "",
            "decisions": "",
            "action_items": "",
            "next_meeting": "",
        }

        lines = minutes_text.split("\n")
        current_section = None

        for line in lines:
            line_lower = line.lower().strip()

            # Detect section headers
            if "meeting title" in line_lower or "title:" in line_lower:
                current_section = "title"
                sections["title"] = (
                    line.split(":", 1)[-1].strip() if ":" in line else line
                )
            elif "date" in line_lower and ":" in line_lower:
                current_section = "date"
                sections["date"] = line.split(":", 1)[-1].strip()
            elif "attendees" in line_lower or "participants" in line_lower:
                current_section = "attendees"
            elif "agenda" in line_lower:
                current_section = "agenda"
            elif "discussion" in line_lower:
                current_section = "discussion"
            elif "decisions" in line_lower:
                current_section = "decisions"
            elif "action items" in line_lower or "action_items" in line_lower:
                current_section = "action_items"
            elif "next meeting" in line_lower:
                current_section = "next_meeting"
            elif current_section and line.strip():
                # Add content to current section
                if sections[current_section]:
                    sections[current_section] += "\n" + line.strip()
                else:
                    sections[current_section] = line.strip()

        return sections

    def get_available_models(self) -> List[str]:
        """Get list of available Anthropic models."""
        return [
            "claude-3-5-sonnet-20241022",
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307",
            "claude-2.1",
            "claude-2.0",
        ]


async def mock_transcript_stream():
    """Mock transcript stream for testing."""
    transcript_parts = [
        "John: Welcome everyone to the Q3 planning meeting.",
        "Sarah: Thanks John. Let's start with the sales numbers.",
        "Mike: Sales are up 15% compared to last quarter.",
        "Lisa: Marketing campaigns have been effective.",
        "John: Great. Now let's discuss the new product launch.",
        "Sarah: The launch is scheduled for November 15th.",
        "Mike: We need to finalize the marketing materials.",
        "Lisa: I'll have the designs ready by next week.",
        "John: Action items: Mike to prepare sales report, Lisa to finalize designs.",
        "Sarah: Next meeting will be in two weeks.",
    ]

    for part in transcript_parts:
        yield part
        await asyncio.sleep(0.2)


async def test_meeting_summary():
    """Test meeting summarization."""
    print("Testing meeting summarization with Anthropic Claude...")

    summarizer = MeetingSummarizer(model="claude-3-haiku-20240307")

    print(f"Using model: {summarizer.model}")
    print(f"Available models: {summarizer.get_available_models()}")

    # Test individual chunk summarization
    test_chunk = """
    John: The quarterly results show strong growth in all regions.
    Sarah: Europe performed particularly well with 25% increase.
    Mike: We need to address supply chain issues in Asia.
    Lisa: Customer satisfaction scores are at an all-time high.
    John: Let's focus on maintaining this momentum.
    """

    print("\nTesting brief summary:")
    brief_summary = await summarizer.summarize_chunk(test_chunk, "brief")
    print(f"Brief summary: {brief_summary}")

    print("\nTesting action items extraction:")
    action_summary = await summarizer.summarize_chunk(test_chunk, "action_items")
    print(f"Action items: {action_summary}")

    # Test streaming summarization
    print("\n\nTesting streaming summarization:")
    summaries = await summarizer.summarize_stream(
        mock_transcript_stream(), style="detailed", chunk_size=5
    )

    print(f"\nGenerated {len(summaries)} summaries from stream")

    # Test meeting minutes generation
    print("\n\nTesting meeting minutes generation:")
    full_transcript = "\n".join(
        [
            "Meeting: Q3 Planning",
            "Date: October 15, 2023",
            "Attendees: John, Sarah, Mike, Lisa",
            "John opened the meeting and reviewed the agenda.",
            "Sarah presented sales numbers showing 15% growth.",
            "Mike discussed supply chain challenges.",
            "Lisa reported on marketing campaign performance.",
            "Decisions: Launch new product on November 15th.",
            "Action items: Mike to prepare report, Lisa to finalize designs.",
            "Next meeting: October 29th.",
        ]
    )

    minutes = await summarizer.generate_meeting_minutes(full_transcript)
    print("\nGenerated meeting minutes:")
    for section, content in minutes.items():
        if content and content.strip():
            print(f"\n{section.upper()}:")
            print(content[:200] + "..." if len(content) > 200 else content)


if __name__ == "__main__":
    asyncio.run(test_meeting_summary())

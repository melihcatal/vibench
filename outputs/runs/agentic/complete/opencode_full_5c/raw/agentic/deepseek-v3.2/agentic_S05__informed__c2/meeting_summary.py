import anthropic
import os
from typing import List, Dict, Any, Optional
import json
from datetime import datetime


class MeetingSummarizer:
    def __init__(self, model: str = "claude-3-5-sonnet-20241022"):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable must be set")

        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = model
        self.summary_history = []

        self.available_models = [
            "claude-3-5-sonnet-20241022",
            "claude-3-5-haiku-20241022",
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307",
        ]

    def validate_model(self) -> bool:
        return self.model in self.available_models

    def create_summary_prompt(
        self, transcript_chunks: List[str], context: Optional[Dict[str, Any]] = None
    ) -> str:
        transcript_text = "\n\n".join(
            [f"Chunk {i + 1}: {chunk}" for i, chunk in enumerate(transcript_chunks)]
        )

        prompt = f"""You are an expert meeting summarizer. Analyze the following meeting transcript chunks and create a comprehensive summary.

Meeting Transcript:
{transcript_text}

Context information:
- Meeting type: {context.get("meeting_type", "General meeting") if context else "General meeting"}
- Participants: {context.get("participants", "Unknown") if context else "Unknown"}
- Duration: {context.get("duration", "Unknown") if context else "Unknown"}
- Date: {context.get("date", datetime.now().strftime("%Y-%m-%d")) if context else datetime.now().strftime("%Y-%m-%d")}

Please provide a structured summary including:
1. Key discussion points and topics covered
2. Decisions made and action items
3. Important questions raised
4. Next steps and follow-ups
5. Any unresolved issues or concerns

Format the summary in clear, concise bullet points. Focus on the most important information."""

        return prompt

    def summarize_transcript(
        self, transcript_chunks: List[str], context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        if not transcript_chunks:
            return {"error": "No transcript chunks provided"}

        prompt = self.create_summary_prompt(transcript_chunks, context)

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0.3,
                messages=[{"role": "user", "content": prompt}],
            )

            summary_text = response.content[0].text

            structured_summary = self._extract_structured_summary(summary_text)

            result = {
                "summary": summary_text,
                "structured_summary": structured_summary,
                "model_used": self.model,
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
                "total_tokens": response.usage.input_tokens
                + response.usage.output_tokens,
                "timestamp": datetime.now().isoformat(),
                "chunk_count": len(transcript_chunks),
                "total_chars": sum(len(chunk) for chunk in transcript_chunks),
            }

            self.summary_history.append(result)
            return result

        except Exception as e:
            return {"error": str(e), "model": self.model}

    def _extract_structured_summary(self, summary_text: str) -> Dict[str, Any]:
        sections = {
            "key_points": [],
            "decisions": [],
            "action_items": [],
            "questions": [],
            "next_steps": [],
            "unresolved_issues": [],
        }

        lines = summary_text.split("\n")
        current_section = None

        for line in lines:
            line = line.strip()
            if not line:
                continue

            lower_line = line.lower()

            if any(
                keyword in lower_line
                for keyword in ["key discussion", "topics covered", "main points"]
            ):
                current_section = "key_points"
            elif any(
                keyword in lower_line for keyword in ["decisions", "agreed", "resolved"]
            ):
                current_section = "decisions"
            elif any(
                keyword in lower_line
                for keyword in ["action items", "tasks", "assignments"]
            ):
                current_section = "action_items"
            elif any(
                keyword in lower_line for keyword in ["questions", "raised", "asked"]
            ):
                current_section = "questions"
            elif any(
                keyword in lower_line
                for keyword in ["next steps", "follow-ups", "follow up"]
            ):
                current_section = "next_steps"
            elif any(
                keyword in lower_line
                for keyword in ["unresolved", "concerns", "issues"]
            ):
                current_section = "unresolved_issues"
            elif line.startswith(("- ", "* ", "• ", "1. ", "2. ", "3. ", "4. ", "5. ")):
                if current_section and current_section in sections:
                    clean_line = line.lstrip("-*• 1234567890.")
                    sections[current_section].append(clean_line.strip())

        return sections

    def summarize_live_meeting(
        self, transcript_stream, chunk_size: int = 10, interval_minutes: int = 5
    ):
        buffer = []
        chunk_counter = 0

        for transcript in transcript_stream:
            if transcript.get("is_final"):
                buffer.append(transcript.get("text", ""))
                chunk_counter += 1

                if chunk_counter >= chunk_size:
                    summary = self.summarize_transcript(buffer)
                    yield {
                        "type": "periodic_summary",
                        "summary": summary,
                        "chunks_processed": chunk_counter,
                        "timestamp": datetime.now().isoformat(),
                    }

                    buffer = buffer[-chunk_size // 2 :]
                    chunk_counter = len(buffer)

        if buffer:
            final_summary = self.summarize_transcript(buffer)
            yield {
                "type": "final_summary",
                "summary": final_summary,
                "total_chunks": len(buffer),
                "timestamp": datetime.now().isoformat(),
            }

    def get_summary_history(self) -> List[Dict[str, Any]]:
        return self.summary_history.copy()

    def clear_history(self):
        self.summary_history.clear()

    def export_summary(self, summary: Dict[str, Any], format: str = "json") -> str:
        if format == "json":
            return json.dumps(summary, indent=2)
        elif format == "text":
            text_output = f"Meeting Summary\n"
            text_output += f"Model: {summary.get('model_used', 'Unknown')}\n"
            text_output += f"Timestamp: {summary.get('timestamp', 'Unknown')}\n"
            text_output += f"Tokens: {summary.get('total_tokens', 0)} (in: {summary.get('input_tokens', 0)}, out: {summary.get('output_tokens', 0)})\n"
            text_output += f"\n{summary.get('summary', 'No summary available')}\n"
            return text_output
        else:
            raise ValueError(f"Unsupported format: {format}")

    def set_model(self, model: str):
        if model not in self.available_models:
            raise ValueError(
                f"Unsupported model: {model}. Available: {self.available_models}"
            )
        self.model = model

    def get_available_models(self) -> List[str]:
        return self.available_models.copy()

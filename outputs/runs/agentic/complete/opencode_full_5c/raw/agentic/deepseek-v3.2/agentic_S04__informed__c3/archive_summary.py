import os
import anthropic
from typing import List, Dict, Any
from speech_models import TranscriptionResult, TimestampedTranscript


def summarize_transcription_results(
    transcript: TranscriptionResult, summary_type: str = "concise"
) -> Dict[str, Any]:
    """
    Summarize transcription results using Anthropic Claude API.

    Args:
        transcript: TranscriptionResult object
        summary_type: Type of summary ("concise", "detailed", "bullet_points", "executive")

    Returns:
        Dictionary with summary and metadata
    """
    # Get Anthropic API key from environment
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")

    # Initialize Anthropic client
    client = anthropic.Anthropic(api_key=api_key)

    # Prepare prompt based on summary type
    prompt_templates = {
        "concise": "Provide a concise 2-3 sentence summary of the following transcript:",
        "detailed": "Provide a detailed summary of the following transcript, covering main topics and key points:",
        "bullet_points": "Provide a summary of the following transcript as bullet points:",
        "executive": "Provide an executive summary of the following transcript suitable for business reporting:",
    }

    if summary_type not in prompt_templates:
        summary_type = "concise"

    prompt = f"{prompt_templates[summary_type]}\n\n{transcript.transcript}"

    try:
        # Call Claude API
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1000,
            temperature=0.3,
            system="You are a helpful assistant that summarizes transcripts accurately and objectively.",
            messages=[{"role": "user", "content": prompt}],
        )

        summary = message.content[0].text

        # Extract key topics if transcript is long enough
        key_topics = []
        if len(transcript.transcript.split()) > 100:
            topics_prompt = f"Extract 3-5 key topics or themes from this transcript:\n\n{transcript.transcript}"

            topics_message = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=500,
                temperature=0.2,
                system="Extract key topics from transcripts.",
                messages=[{"role": "user", "content": topics_prompt}],
            )

            key_topics = [
                topic.strip()
                for topic in topics_message.content[0].text.split("\n")
                if topic.strip()
            ]

        # Calculate statistics
        word_count = len(transcript.transcript.split())
        char_count = len(transcript.transcript)

        # Get speaker statistics if available
        speaker_stats = {}
        if hasattr(transcript, "speaker_segments") and transcript.speaker_segments:
            speakers = {}
            for segment in transcript.speaker_segments:
                speaker = segment.get("speaker_label", "Unknown")
                if speaker not in speakers:
                    speakers[speaker] = 0
                speakers[speaker] += segment.get("end_time", 0) - segment.get(
                    "start_time", 0
                )

            speaker_stats = {
                "total_speakers": len(speakers),
                "speaking_time_distribution": speakers,
            }

        return {
            "job_id": transcript.job_id,
            "summary_type": summary_type,
            "summary": summary,
            "key_topics": key_topics,
            "statistics": {
                "word_count": word_count,
                "character_count": char_count,
                "language": transcript.language_code,
                **speaker_stats,
            },
            "model_used": "claude-3-haiku-20240307",
            "prompt_tokens": message.usage.input_tokens,
            "completion_tokens": message.usage.output_tokens,
            "total_tokens": message.usage.input_tokens + message.usage.output_tokens,
        }

    except anthropic.APIError as e:
        print(f"Error calling Anthropic API: {e}")
        raise


def generate_meeting_minutes(
    transcript: TranscriptionResult, include_actions: bool = True
) -> Dict[str, Any]:
    """
    Generate meeting minutes from transcript using Anthropic Claude.

    Args:
        transcript: TranscriptionResult object
        include_actions: Whether to extract action items

    Returns:
        Dictionary with meeting minutes
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")

    client = anthropic.Anthropic(api_key=api_key)

    # Prepare transcript with speaker information if available
    transcript_text = transcript.transcript

    if hasattr(transcript, "speaker_segments") and transcript.speaker_segments:
        # Enhance transcript with speaker labels
        import re

        words_with_speakers = []

        # This is a simplified version - in production you'd map words to speakers
        transcript_text = f"Meeting transcript with {len(set(s['speaker_label'] for s in transcript.speaker_segments))} participants:\n\n{transcript_text}"

    prompt = f"""Generate comprehensive meeting minutes from the following transcript.
    
    Include:
    1. Meeting overview and date/time (if mentioned)
    2. List of participants (if identifiable)
    3. Key discussion points
    4. Decisions made
    5. Action items with owners and deadlines (if mentioned)
    6. Next steps
    
    Transcript:
    {transcript_text}
    """

    try:
        message = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=2000,
            temperature=0.2,
            system="You are an expert at creating professional meeting minutes from transcripts.",
            messages=[{"role": "user", "content": prompt}],
        )

        minutes = message.content[0].text

        # Extract action items separately if requested
        action_items = []
        if include_actions:
            actions_prompt = f"""Extract all action items from this meeting transcript.
            Format each as: [Owner] - [Action] - [Deadline if mentioned]
            
            Transcript:
            {transcript_text}
            """

            actions_message = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=500,
                temperature=0.1,
                system="Extract action items from meeting transcripts.",
                messages=[{"role": "user", "content": actions_prompt}],
            )

            action_items = [
                item.strip()
                for item in actions_message.content[0].text.split("\n")
                if item.strip()
            ]

        return {
            "job_id": transcript.job_id,
            "meeting_minutes": minutes,
            "action_items": action_items,
            "model_used": "claude-3-sonnet-20240229",
            "token_usage": {
                "input_tokens": message.usage.input_tokens,
                "output_tokens": message.usage.output_tokens,
                "total_tokens": message.usage.input_tokens
                + message.usage.output_tokens,
            },
        }

    except anthropic.APIError as e:
        print(f"Error generating meeting minutes: {e}")
        raise


if __name__ == "__main__":
    # Example usage
    import sys

    # Check for Anthropic API key
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Please set ANTHROPIC_API_KEY environment variable")
        sys.exit(1)

    if len(sys.argv) > 1:
        # Create a mock transcript for testing
        mock_transcript = TranscriptionResult(
            job_id="test-job-123", transcript=sys.argv[1], language_code="en-US"
        )

        result = summarize_transcription_results(mock_transcript, "concise")
        print(f"Summary: {result['summary']}")
        print(f"Key topics: {result['key_topics']}")
    else:
        print("Usage: python archive_summary.py <transcript_text>")
        print("Example: python archive_summary.py 'Meeting discussed Q3 results...'")

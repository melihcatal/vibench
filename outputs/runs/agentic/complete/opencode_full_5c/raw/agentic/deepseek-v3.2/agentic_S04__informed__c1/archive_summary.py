import anthropic
import os
from typing import Dict, Any, List, Optional
import json


def summarize_transcription_results(
    transcript_data: Dict[str, Any], summary_type: str = "meeting"
) -> Dict[str, Any]:
    """
    Summarize transcription results using Anthropic Claude API.

    Args:
        transcript_data: Transcript data from poll_transcription_job
        summary_type: Type of summary ("meeting", "interview", "lecture", "general")

    Returns:
        Summary with key points, action items, and metadata
    """
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    transcript_text = transcript_data.get("transcript", "")

    if not transcript_text.strip():
        return {
            "error": "Empty transcript",
            "summary": "",
            "key_points": [],
            "action_items": [],
        }

    prompt_mapping = {
        "meeting": "Summarize this meeting transcript. Extract key decisions, action items, and important discussion points.",
        "interview": "Summarize this interview transcript. Extract key insights, candidate qualifications, and important questions/answers.",
        "lecture": "Summarize this lecture transcript. Extract main topics, key concepts, and important takeaways.",
        "general": "Summarize this transcript concisely, highlighting the main points and key information.",
    }

    system_prompt = """You are a helpful assistant that summarizes transcripts. 
    Provide a concise summary, extract key points as bullet points, 
    and identify any action items or decisions mentioned."""

    user_prompt = f"""{prompt_mapping.get(summary_type, prompt_mapping["general"])}

Transcript:
{transcript_text[:15000]}

Please provide:
1. A concise summary (2-3 paragraphs)
2. Key points (bullet points)
3. Action items or decisions (if any)
4. Participants mentioned (if any)"""

    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1000,
            temperature=0.3,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )

        summary_text = response.content[0].text

        return {
            "summary": summary_text,
            "summary_type": summary_type,
            "model_used": "claude-3-haiku-20240307",
            "transcript_length": len(transcript_text),
            "summary_length": len(summary_text),
            "parsed_summary": parse_summary_response(summary_text),
        }

    except Exception as e:
        return {"error": str(e), "summary": "", "key_points": [], "action_items": []}


def parse_summary_response(summary_text: str) -> Dict[str, Any]:
    """
    Parse the summary response into structured components.

    Args:
        summary_text: Raw summary text from Claude

    Returns:
        Structured summary components
    """
    lines = summary_text.split("\n")

    sections = {
        "concise_summary": "",
        "key_points": [],
        "action_items": [],
        "participants": [],
    }

    current_section = None

    for line in lines:
        line = line.strip()

        if not line:
            continue

        lower_line = line.lower()

        if "summary:" in lower_line or ("1." in line and "summary" in lower_line):
            current_section = "concise_summary"
            line = line.split(":", 1)[-1].strip() if ":" in line else line
            if line:
                sections["concise_summary"] += line + " "
        elif "key points:" in lower_line or ("2." in line and "key" in lower_line):
            current_section = "key_points"
        elif "action items:" in lower_line or ("3." in line and "action" in lower_line):
            current_section = "action_items"
        elif "participants:" in lower_line or (
            "4." in line and "participants" in lower_line
        ):
            current_section = "participants"
        elif current_section == "concise_summary":
            sections["concise_summary"] += line + " "
        elif current_section == "key_points" and (
            line.startswith("-") or line.startswith("•") or line.startswith("*")
        ):
            point = line[1:].strip()
            if point:
                sections["key_points"].append(point)
        elif current_section == "action_items" and (
            line.startswith("-") or line.startswith("•") or line.startswith("*")
        ):
            item = line[1:].strip()
            if item:
                sections["action_items"].append(item)
        elif current_section == "participants" and (
            line.startswith("-") or line.startswith("•") or line.startswith("*")
        ):
            participant = line[1:].strip()
            if participant:
                sections["participants"].append(participant)

    sections["concise_summary"] = sections["concise_summary"].strip()

    return sections


def generate_meeting_minutes(transcript_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate formal meeting minutes from transcript.

    Args:
        transcript_data: Transcript data

    Returns:
        Structured meeting minutes
    """
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    transcript_text = transcript_data.get("transcript", "")

    system_prompt = """You are a professional meeting minutes recorder. 
    Generate formal meeting minutes in JSON format with the following structure:
    {
        "meeting_title": "string",
        "date": "string (extracted or inferred)",
        "attendees": ["list of names"],
        "absent": ["list of names if mentioned"],
        "agenda_items": [
            {
                "topic": "string",
                "discussion": "string",
                "decisions": ["list of decisions"],
                "action_items": [
                    {
                        "action": "string",
                        "assignee": "string",
                        "due_date": "string (if mentioned)"
                    }
                ]
            }
        ],
        "next_meeting": "string (if mentioned)"
    }"""

    user_prompt = f"""Convert this meeting transcript into formal meeting minutes in JSON format:

Transcript:
{transcript_text[:10000]}

Extract all relevant information for meeting minutes. If information is not available in the transcript, use "Not specified" or empty arrays as appropriate."""

    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1500,
            temperature=0.2,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )

        minutes_text = response.content[0].text

        try:
            json_start = minutes_text.find("{")
            json_end = minutes_text.rfind("}") + 1
            if json_start >= 0 and json_end > json_start:
                json_str = minutes_text[json_start:json_end]
                minutes_data = json.loads(json_str)
            else:
                minutes_data = {"raw_response": minutes_text}
        except json.JSONDecodeError:
            minutes_data = {
                "raw_response": minutes_text,
                "parse_error": "Could not parse JSON",
            }

        return {
            "minutes": minutes_data,
            "model_used": "claude-3-haiku-20240307",
            "transcript_length": len(transcript_text),
        }

    except Exception as e:
        return {"error": str(e), "minutes": {}}


def create_transcript_archive(
    transcript_data: Dict[str, Any],
    include_summary: bool = True,
    include_minutes: bool = False,
) -> Dict[str, Any]:
    """
    Create a comprehensive archive of transcription results.

    Args:
        transcript_data: Transcript data
        include_summary: Whether to include AI summary
        include_minutes: Whether to include meeting minutes

    Returns:
        Complete archive package
    """
    archive = {
        "metadata": {
            "transcript_source": "Amazon Transcribe",
            "job_name": transcript_data.get("job_name"),
            "language_code": transcript_data.get("language_code", "en-US"),
            "word_count": len(transcript_data.get("items", [])),
            "speaker_count": len(transcript_data.get("speakers", [])),
            "timestamp": transcript_data.get("timestamp"),
        },
        "transcript": {
            "full_text": transcript_data.get("transcript", ""),
            "segments": transcript_data.get("speakers", []),
        },
    }

    if include_summary:
        summary = summarize_transcription_results(transcript_data)
        archive["summary"] = summary

    if include_minutes:
        minutes = generate_meeting_minutes(transcript_data)
        archive["meeting_minutes"] = minutes

    if "items" in transcript_data:
        word_timestamps = [
            {
                "word": item["alternatives"][0]["content"],
                "start_time": item.get("start_time"),
                "end_time": item.get("end_time"),
                "confidence": item["alternatives"][0].get("confidence"),
            }
            for item in transcript_data["items"]
            if item["type"] == "pronunciation"
        ]
        archive["word_timestamps"] = word_timestamps

    return archive

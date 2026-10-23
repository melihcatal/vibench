import os
from typing import Dict, Any, List
from openai import OpenAI
from speech_models import NormalizedTranscript


def archive_summary(
    transcript: NormalizedTranscript, summary_type: str = "concise"
) -> Dict[str, Any]:
    """
    Summarize transcription results using OpenAI GPT.

    Args:
        transcript: Normalized transcript to summarize
        summary_type: Type of summary - "concise", "detailed", "bullet_points", "key_points"

    Returns:
        Dictionary with summary and metadata
    """
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise EnvironmentError(
            "OpenAI API key not found. Please set OPENAI_API_KEY environment variable."
        )

    client = OpenAI(api_key=openai_api_key)

    prompt_templates = {
        "concise": "Provide a concise summary (2-3 sentences) of the following transcript:\n\n{text}",
        "detailed": "Provide a detailed summary of the following transcript, covering main topics and key points:\n\n{text}",
        "bullet_points": "Extract key bullet points from the following transcript:\n\n{text}",
        "key_points": "Identify the 5 most important key points from the following transcript:\n\n{text}",
    }

    if summary_type not in prompt_templates:
        raise ValueError(
            f"Invalid summary_type: {summary_type}. Must be one of: {list(prompt_templates.keys())}"
        )

    chunks = split_into_chunks_for_summary(transcript)
    summaries = []

    for i, chunk in enumerate(chunks):
        try:
            prompt = prompt_templates[summary_type].format(text=chunk)

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that summarizes transcripts accurately.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=500,
                temperature=0.3,
            )

            summary = response.choices[0].message.content.strip()
            summaries.append(
                {
                    "chunk_index": i,
                    "summary": summary,
                    "token_count": response.usage.total_tokens if response.usage else 0,
                }
            )

        except Exception as e:
            raise Exception(f"OpenAI API error for chunk {i}: {e}")

    combined_summary = combine_summaries(summaries, summary_type)

    return {
        "summary_type": summary_type,
        "summary": combined_summary,
        "chunk_summaries": summaries,
        "transcript_length": len(transcript.text),
        "segment_count": len(transcript.segments),
        "duration_seconds": transcript.duration_seconds,
    }


def split_into_chunks_for_summary(
    transcript: NormalizedTranscript, max_tokens: int = 3000
) -> List[str]:
    """
    Split transcript into chunks suitable for summarization.

    Args:
        transcript: Normalized transcript
        max_tokens: Maximum tokens per chunk

    Returns:
        List of text chunks
    """
    text = transcript.text
    estimated_tokens = len(text) // 4

    if estimated_tokens <= max_tokens:
        return [text]

    chunks = []
    paragraphs = text.split("\n\n")
    current_chunk = ""
    current_tokens = 0

    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue

        paragraph_tokens = len(paragraph) // 4

        if current_tokens + paragraph_tokens <= max_tokens:
            current_chunk += "\n\n" + paragraph if current_chunk else paragraph
            current_tokens += paragraph_tokens
        else:
            if current_chunk:
                chunks.append(current_chunk)

            if paragraph_tokens > max_tokens:
                sentences = paragraph.split(". ")
                sub_chunk = ""
                sub_tokens = 0

                for sentence in sentences:
                    sentence = sentence.strip()
                    if not sentence:
                        continue

                    if sentence[-1] != ".":
                        sentence += "."

                    sentence_tokens = len(sentence) // 4

                    if sub_tokens + sentence_tokens <= max_tokens:
                        sub_chunk += " " + sentence if sub_chunk else sentence
                        sub_tokens += sentence_tokens
                    else:
                        if sub_chunk:
                            chunks.append(sub_chunk)
                        sub_chunk = sentence
                        sub_tokens = sentence_tokens

                if sub_chunk:
                    current_chunk = sub_chunk
                    current_tokens = sub_tokens
            else:
                current_chunk = paragraph
                current_tokens = paragraph_tokens

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def combine_summaries(chunk_summaries: List[Dict[str, Any]], summary_type: str) -> str:
    """
    Combine multiple chunk summaries into a coherent whole.

    Args:
        chunk_summaries: List of chunk summaries
        summary_type: Type of summary

    Returns:
        Combined summary text
    """
    if not chunk_summaries:
        return ""

    if len(chunk_summaries) == 1:
        return chunk_summaries[0]["summary"]

    if summary_type == "bullet_points":
        all_points = []
        for summary in chunk_summaries:
            points = summary["summary"].split("\n")
            all_points.extend([p.strip() for p in points if p.strip()])
        return "\n".join(all_points)

    elif summary_type == "key_points":
        all_points = []
        for summary in chunk_summaries:
            points = summary["summary"].split("\n")
            all_points.extend([p.strip() for p in points if p.strip()])
        return "\n".join(all_points[:5])

    else:
        combined = " ".join([s["summary"] for s in chunk_summaries])
        return combined

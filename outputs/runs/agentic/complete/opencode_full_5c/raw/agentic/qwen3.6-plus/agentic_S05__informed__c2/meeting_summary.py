import os
from typing import List, Optional

import dashscope
from dashscope import Generation

from speech_models import TranscriptResult

QWEN_MODEL = "qwen-turbo"


def get_dashscope_api_key() -> str:
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY environment variable is not set")
    return api_key


def configure_dashscope(api_key: Optional[str] = None):
    key = api_key or get_dashscope_api_key()
    dashscope.api_key = key


def build_meeting_prompt(
    transcript_chunks: List[str],
    summary_type: str = "comprehensive",
    language: str = "en",
) -> str:
    full_transcript = "\n".join(transcript_chunks)

    prompts = {
        "comprehensive": (
            f"Please provide a comprehensive summary of the following meeting transcript. "
            f"Include key discussion points, decisions made, action items, and any important context. "
            f"Format the summary with clear sections.\n\n"
            f"Meeting Transcript:\n{full_transcript}"
        ),
        "action_items": (
            f"Extract all action items from the following meeting transcript. "
            f"For each action item, identify the responsible person (if mentioned), "
            f"the task description, and any deadlines discussed.\n\n"
            f"Meeting Transcript:\n{full_transcript}"
        ),
        "key_decisions": (
            f"Identify all key decisions made during this meeting from the transcript below. "
            f"For each decision, provide context about what was discussed and why the decision was made.\n\n"
            f"Meeting Transcript:\n{full_transcript}"
        ),
        "brief": (
            f"Provide a brief 2-3 paragraph summary of the following meeting transcript, "
            f"focusing on the main topics discussed and outcomes.\n\n"
            f"Meeting Transcript:\n{full_transcript}"
        ),
    }

    return prompts.get(summary_type, prompts["comprehensive"])


def summarize_meeting(
    transcript_chunks: List[str],
    model: str = QWEN_MODEL,
    summary_type: str = "comprehensive",
    language: str = "en",
    max_tokens: int = 2000,
    temperature: float = 0.3,
    api_key: Optional[str] = None,
) -> str:
    configure_dashscope(api_key)

    prompt = build_meeting_prompt(transcript_chunks, summary_type, language)

    messages = [
        {
            "role": "system",
            "content": "You are a professional meeting summarizer assistant.",
        },
        {"role": "user", "content": prompt},
    ]

    response = Generation.call(
        model=model,
        messages=messages,
        result_format="message",
        max_tokens=max_tokens,
        temperature=temperature,
    )

    if response.status_code == 200:
        return response.output.choices[0].message.content
    else:
        raise RuntimeError(
            f"DashScope Qwen API error: {response.code} - {response.message}"
        )


def summarize_live_transcripts(
    results: List[TranscriptResult],
    model: str = QWEN_MODEL,
    summary_type: str = "comprehensive",
    language: str = "en",
    max_tokens: int = 2000,
    temperature: float = 0.3,
    api_key: Optional[str] = None,
) -> str:
    final_chunks = [r.text for r in results if r.is_final and r.text.strip()]
    if not final_chunks:
        all_chunks = [r.text for r in results if r.text.strip()]
        if all_chunks:
            return " ".join(all_chunks)
        return ""

    return summarize_meeting(
        transcript_chunks=final_chunks,
        model=model,
        summary_type=summary_type,
        language=language,
        max_tokens=max_tokens,
        temperature=temperature,
        api_key=api_key,
    )


class MeetingSummarizer:
    def __init__(
        self,
        model: str = QWEN_MODEL,
        summary_type: str = "comprehensive",
        language: str = "en",
        max_tokens: int = 2000,
        temperature: float = 0.3,
        api_key: Optional[str] = None,
    ):
        self.model = model
        self.summary_type = summary_type
        self.language = language
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.api_key = api_key
        self._transcript_chunks: List[str] = []
        self._summaries: List[str] = []

    def add_chunk(self, result: TranscriptResult):
        if result.text.strip():
            self._transcript_chunks.append(result.text)

    def add_text(self, text: str):
        if text.strip():
            self._transcript_chunks.append(text)

    def summarize(self) -> str:
        if not self._transcript_chunks:
            return ""

        summary = summarize_meeting(
            transcript_chunks=self._transcript_chunks,
            model=self.model,
            summary_type=self.summary_type,
            language=self.language,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            api_key=self.api_key,
        )
        self._summaries.append(summary)
        return summary

    def summarize_and_clear(self) -> str:
        summary = self.summarize()
        self._transcript_chunks.clear()
        return summary

    def get_transcript(self) -> str:
        return " ".join(self._transcript_chunks)

    def get_all_summaries(self) -> List[str]:
        return self._summaries.copy()

    def clear(self):
        self._transcript_chunks.clear()
        self._summaries.clear()

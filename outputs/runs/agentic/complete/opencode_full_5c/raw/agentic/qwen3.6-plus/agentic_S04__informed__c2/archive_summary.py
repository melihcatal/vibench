import dashscope
from dashscope import Generation

from speech_client import load_dashscope_config
from speech_models import (
    SummaryResult,
    normalize_dashscope_summary,
)


def summarize_transcription(
    text: str, model: str = None, max_tokens: int = 500
) -> SummaryResult:
    config = load_dashscope_config()
    dashscope.api_key = config.api_key

    model_name = model or config.default_model

    prompt = (
        f"Please provide a concise summary of the following meeting transcription. "
        f"Include key topics discussed, decisions made, and any action items mentioned.\n\n"
        f"Transcription:\n{text}"
    )

    response = Generation.call(
        model=model_name,
        prompt=prompt,
        max_tokens=max_tokens,
        result_format="message",
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"DashScope Qwen API error: {response.code} - {response.message}"
        )

    output_text = (
        response.output.text if response.output and response.output.text else ""
    )

    return SummaryResult(
        summary=output_text,
        key_topics=[],
        action_items=[],
        sentiment="neutral",
    )


def summarize_with_qwen_plus(text: str, max_tokens: int = 1000) -> SummaryResult:
    config = load_dashscope_config()
    dashscope.api_key = config.api_key

    prompt = (
        f"Analyze the following meeting transcription and provide:\n"
        f"1. A concise executive summary\n"
        f"2. Key topics discussed (as bullet points)\n"
        f"3. Action items with responsible parties if mentioned\n"
        f"4. Overall sentiment of the meeting\n\n"
        f"Transcription:\n{text}"
    )

    response = Generation.call(
        model="qwen-plus",
        prompt=prompt,
        max_tokens=max_tokens,
        result_format="message",
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"DashScope Qwen API error: {response.code} - {response.message}"
        )

    output_text = (
        response.output.text if response.output and response.output.text else ""
    )

    return SummaryResult(
        summary=output_text,
        key_topics=[],
        action_items=[],
        sentiment="neutral",
    )


def generate_meeting_archive_summary(
    transcription_text: str, meeting_title: str = None, model: str = None
) -> SummaryResult:
    config = load_dashscope_config()
    dashscope.api_key = config.api_key

    model_name = model or config.default_model

    title_context = f"Meeting: {meeting_title}\n\n" if meeting_title else ""

    prompt = (
        f"{title_context}"
        f"Create a comprehensive archive summary of this meeting transcription. "
        f"Include a summary, key discussion points, decisions, and action items. "
        f"Format the output clearly for archival purposes.\n\n"
        f"Transcription:\n{transcription_text}"
    )

    response = Generation.call(
        model=model_name,
        prompt=prompt,
        max_tokens=1500,
        result_format="message",
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"DashScope Qwen API error: {response.code} - {response.message}"
        )

    output_text = (
        response.output.text if response.output and response.output.text else ""
    )

    return SummaryResult(
        summary=output_text,
        key_topics=[],
        action_items=[],
        sentiment="neutral",
    )

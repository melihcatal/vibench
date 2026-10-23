import os
from typing import Optional, Dict, Any

from anthropic import Anthropic


def stored_asset_summary(
    extracted_text: str,
    asset_name: str = "document",
    summary_length: str = "medium",
    focus_areas: Optional[list] = None,
) -> Dict[str, Any]:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return {
            "success": False,
            "error": "ANTHROPIC_API_KEY environment variable not set",
        }

    client = Anthropic(api_key=api_key)

    length_instructions = {
        "short": "Provide a brief 2-3 sentence summary.",
        "medium": "Provide a concise paragraph summary of 5-7 sentences.",
        "long": "Provide a detailed multi-paragraph summary covering all key points.",
    }

    instruction = length_instructions.get(summary_length, length_instructions["medium"])

    system_prompt = (
        "You are a document analysis assistant. "
        "Summarize the provided text accurately and objectively."
    )

    focus_text = ""
    if focus_areas:
        focus_text = f"Pay special attention to: {', '.join(focus_areas)}."

    user_message = (
        f"{instruction}\n\n"
        f"{focus_text}\n\n"
        f"Document: {asset_name}\n\n"
        f"Content:\n{extracted_text}"
    )

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_message},
            ],
        )

        summary_text = ""
        for content_block in message.content:
            if content_block.type == "text":
                summary_text += content_block.text

        return {
            "success": True,
            "asset_name": asset_name,
            "summary": summary_text,
            "summary_length": summary_length,
            "model": "claude-sonnet-4-20250514",
            "stop_reason": message.stop_reason,
            "input_tokens": message.usage.input_tokens,
            "output_tokens": message.usage.output_tokens,
        }
    except Exception as exc:
        return {
            "success": False,
            "asset_name": asset_name,
            "error": str(exc),
            "model": "claude-sonnet-4-20250514",
        }

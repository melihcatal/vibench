import json
import os
import requests
from typing import Optional

DASHSCOPE_CHAT_URL = (
    "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
)
QWEN_TEXT_MODEL = "qwen-plus"

SUMMARIZE_PROMPT = (
    "You are a visual analysis summarizer. Given the following image analysis results, "
    "produce a concise structured summary that covers:\n"
    "1. Key visual elements detected\n"
    "2. Any text found in the image\n"
    "3. Safety assessment outcome\n"
    "4. Overall description\n\n"
    "Keep the summary under 150 words. Use clear, objective language."
)


def summarize_visual_analysis(
    labels: list,
    description: str,
    detected_text: str,
    safety_result: dict,
) -> dict:
    """Summarize visual analysis results using DashScope Qwen text model.

    Uses the qwen-plus model hosted on DashScope (Alibaba Cloud).
    Requires DASHSCOPE_API_KEY environment variable.
    """
    api_key = os.environ.get("DASHSCOPE_API_KEY", "")
    if not api_key:
        raise ValueError(
            "DASHSCOPE_API_KEY environment variable is required for DashScope Qwen"
        )

    analysis_input = (
        f"Detected Labels: {', '.join(str(l) for l in labels)}\n"
        f"Description: {description}\n"
        f"Detected Text: {detected_text}\n"
        f"Safety Assessment: {json.dumps(safety_result)}"
    )

    payload = {
        "model": QWEN_TEXT_MODEL,
        "input": {
            "messages": [
                {"role": "system", "content": SUMMARIZE_PROMPT},
                {"role": "user", "content": analysis_input},
            ]
        },
        "parameters": {
            "max_tokens": 512,
            "temperature": 0.3,
        },
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        DASHSCOPE_CHAT_URL,
        headers=headers,
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    response_json = response.json()

    choices = response_json.get("output", {}).get("choices", [])
    summary_text = ""
    if choices:
        summary_text = choices[0].get("message", {}).get("content", "").strip()

    return {
        "summary": summary_text,
        "model": QWEN_TEXT_MODEL,
        "source_labels": labels,
        "source_description": description,
        "source_text": detected_text,
        "source_safety": safety_result,
    }


if __name__ == "__main__":
    result = summarize_visual_analysis(
        labels=["person", "outdoor", "building"],
        description="A person standing in front of a modern building.",
        detected_text="Welcome to City Hall",
        safety_result={"overall_safe": True, "categories": []},
    )
    print(json.dumps(result))

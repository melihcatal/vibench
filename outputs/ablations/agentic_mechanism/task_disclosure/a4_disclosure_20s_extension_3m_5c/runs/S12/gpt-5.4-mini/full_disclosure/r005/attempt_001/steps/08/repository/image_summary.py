import base64
import json
import os
import urllib.request


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_VISION_MODEL = os.getenv("OPENAI_VISION_MODEL", "gpt-4.1-mini")


def _image_to_data_url(image_path):
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("ascii")
    mime_type = "image/jpeg"
    return f"data:{mime_type};base64,{encoded}"


def _extract_summary_text(payload):
    choices = payload.get("choices") or []
    if not choices:
        return ""
    message = choices[0].get("message") or {}
    text = message.get("content") or ""
    return text.strip()


def summarize_image_analysis(image_path, analysis_results=None, mime_type="image/jpeg"):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    analysis_text = ""
    if analysis_results is not None:
        if isinstance(analysis_results, str):
            analysis_text = analysis_results.strip()
        else:
            analysis_text = json.dumps(analysis_results, ensure_ascii=False, sort_keys=True)

    prompt = (
        "Summarize the visual analysis results for this image in 1-3 concise sentences. "
        "Focus on the most important objects, scene context, text, and any safety-relevant details."
    )
    if analysis_text:
        prompt = f"{prompt}\n\nAnalysis results:\n{analysis_text}"

    payload = {
        "model": OPENAI_VISION_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": _image_to_data_url(image_path), "detail": "low"}},
                ],
            }
        ],
        "max_tokens": 120,
        "temperature": 0.2,
    }
    request = urllib.request.Request(
        OPENAI_API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        data = json.load(response)
    return _extract_summary_text(data)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        raise SystemExit("usage: image_summary.py IMAGE_PATH [ANALYSIS_JSON_OR_TEXT]")
    image_path = sys.argv[1]
    analysis = sys.argv[2] if len(sys.argv) > 2 else None
    print(summarize_image_analysis(image_path, analysis))

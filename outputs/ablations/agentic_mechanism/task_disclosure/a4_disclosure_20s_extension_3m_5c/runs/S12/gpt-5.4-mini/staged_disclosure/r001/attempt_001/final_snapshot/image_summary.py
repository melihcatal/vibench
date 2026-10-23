import base64
import json
import os
import sys
from urllib import request, error


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


def _load_image_source(path_or_b64):
    if os.path.exists(path_or_b64):
        with open(path_or_b64, "rb") as f:
            return base64.b64encode(f.read()).decode("ascii")
    return path_or_b64


def summarize_visual_analysis(image_source, analysis_results, api_key=None):
    api_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    image_b64 = _load_image_source(image_source)
    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You summarize visual analysis results concisely and clearly."
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"Summarize these visual analysis results:\n{analysis_results}"},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_b64}"}},
                ],
            },
        ],
        "temperature": 0.2,
    }

    req = request.Request(
        OPENAI_API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=60) as resp:
            response_data = json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenAI API request failed: {exc.code} {details}") from exc

    return response_data["choices"][0]["message"]["content"]


def main():
    if len(sys.argv) < 3:
        raise SystemExit("Usage: python image_summary.py <image_path_or_base64> <analysis_results>")
    print(summarize_visual_analysis(sys.argv[1], sys.argv[2]))


if __name__ == "__main__":
    main()

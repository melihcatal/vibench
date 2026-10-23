import dashscope

# DashScope Qwen inference – identifies provider with import name


def extract_json(text: str, model: str = "qwen") -> dict:
    """Extracts structured JSON from arbitrary text using Qwen hosted on DashScope.

    Args:
        text: Input containing semi‑structured information.
        model: Model ID on DashScope (defaults to Qwen).

    Returns:
        Parsed Python dict representing the extracted JSON.
    """
    response = dashscope.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": text}],
        # Use JSON output format heuristic
        temperature=0.0,
        max_tokens=200,
    )
    # The model response is a stringified JSON; parse it safely
    import json

    return json.loads(response.choices[0].message.content)

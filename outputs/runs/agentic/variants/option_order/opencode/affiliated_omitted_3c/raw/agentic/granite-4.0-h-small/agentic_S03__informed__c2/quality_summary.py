import json
from typing import List, Dict, Any

# Hosted LLM Inference example: Qwen via DashScope
# Uses the dashscope SDK for hosted model inference


def summarize_quality(translated_segments: List[str]) -> Dict[str, Any]:
    """Summarize translation quality issues using a hosted LLM (Qwen).

    Args:
        translated_segments: List of translated text segments.

    Returns:
        A dict outlining detected quality concerns (e.g., fluency, adequacy, toxicity).
    """
    # Import the dashscope client within the function to keep dependency isolated
    from dashscope import ChatCompletion

    # Ensure DashScope API key is available as an environment variable
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise RuntimeError("DASHSCOPE_API_KEY environment variable not set")

    # Configure the DashScope client (no region required for public API)
    chat_completion = ChatCompletion(api_key=api_key)

    # Build a concise prompt that instructs the LLM to assess quality
    # The system message provides role instructions; user messages list the segments
    system_prompt = "You are a language quality assessor. For each segment provide a brief evaluation covering:\n- fluency\n- adequacy\n- naturalness\n- potential toxicity or unsafe content.\nSummaries should be concise (1-2 sentences) and include a confidence score from 0.0 to 1.0."
    user_messages = [
        {
            "role": "user",
            "content": "评估以下翲译文段："
            + "\n".join(f"- {seg}" for seg in translated_segments),
        }
    ]

    # Call the model (Qwen-1.5-72B for demonstration)
    response = chat_completion.chat(
        model="qwen-1.5-72b",
        system=system_prompt,
        messages=user_messages,
        temperature=0.2,
    )

    # The service returns a JSON‑like structure; we parse it here
    answer = response.get("choices", [{}])[0].get("message", {}).get("content", "")
    # Simple attempt to structure the answer as a list of segment evaluations
    evaluations = []
    try:
        # Expecting JSON; otherwise fallback to raw text split
        evaluations = json.loads(answer)
    except json.JSONDecodeError:
        # Fallback: split by line breaks and treat each line as an evaluation block
        for line in answer.strip().split("\n"):
            if line.strip():
                evaluations.append(line)

    # Build a summary dict
    summary = {
        "evaluations": evaluations,
        "overall_confidence": max(
            0.0,
            min(1.0, float(response.get("usage", {}).get("lastTokenUsage", 0) / 1000)),
        ),  # placeholder heuristic
    }
    return summary


# Example usage (requires DASHSCOPE_API_KEY set in env)
if __name__ == "__main__":
    samples = [
        "This is a good translation.",
        "This sentence feels off.",
        "Potential toxicity here?",
    ]
    print(json.dumps(summarize_quality(samples), ensure_ascii=False, indent=2))

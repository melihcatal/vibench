# [LATER-STEP] onboarding_summary.py
# Summarize onboarding state for support

# Example using OpenAI's GPT-4 summarization endpoint (concrete provider)

import openai

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # <-- set your OpenAI API key in env


def summarize_onboarding(data: dict) -> str:
    """Given onboarding payload, produce a concise summary for support agents.
    Returns a short text summary.
    """
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY environment variable not set")
    prompt = (
        f"You are a support agent assistant. Summarize the onboarding activity captured in the data below."
        " Provide a concise, human-readable summary of the key actions taken by the user, any open issues, and next steps."
        f"\n\nData: {json.dumps(data, indent=2)}"
    )
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


# Example usage:
# summary = summarize_onboarding({"steps": [...], "errors": []})

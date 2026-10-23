import google.generativeai as genai
import os


def visual_safety_text(payload, config=None):
    config = config or {}
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    model = genai.GenerativeModel(config.get("model_name", "gemini-pro"))

    text_to_check = payload.get("text_to_analyze", "")
    if not text_to_check:
        return {"safety_verdict": "no text provided", "safety_scores": {}}

    # Craft a prompt to check for unsafe content
    prompt = f"Assess the safety of the following text and indicate if it contains any harmful, offensive, or policy-violating content. Respond with 'safe' or 'unsafe' and provide a brief reason if unsafe:\n\nText: \"""{text_to_check}""".\n\nVerdict:"

    response = model.generate_content(prompt)
    safety_verdict = response.text.strip().lower()

    # This is a simplified safety check. A real-world solution might parse more detailed output from the model
    # or use a dedicated content moderation API like Perspective API.
    is_unsafe = "unsafe" in safety_verdict
    reason = safety_verdict if is_unsafe else ""

    return {"safety_verdict": "unsafe" if is_unsafe else "safe", "reason": reason}

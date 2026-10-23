import os
from typing import List
import google.generativeai as genai
from safety_models import ModerationResponse


def moderation_summary(decisions: List[ModerationResponse]) -> str:
    try:
        api_key = os.environ["GOOGLE_API_KEY"]
    except KeyError:
        raise ValueError("Missing environment variable: GOOGLE_API_KEY")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = "Summarize the following content moderation decisions into a brief report for a human reviewer:\n\n"
    for i, decision in enumerate(decisions):
        prompt += f"Item {i + 1}:\n"
        if not decision.success:
            prompt += "  - Moderation check failed.\n"
            continue
        flags = []
        if decision.hate and decision.hate.severity > 0:
            flags.append(f"Hate (severity: {decision.hate.severity})")
        if decision.self_harm and decision.self_harm.severity > 0:
            flags.append(f"Self-Harm (severity: {decision.self_harm.severity})")
        if decision.sexual and decision.sexual.severity > 0:
            flags.append(f"Sexual (severity: {decision.sexual.severity})")
        if decision.violence and decision.violence.severity > 0:
            flags.append(f"Violence (severity: {decision.violence.severity})")

        if flags:
            prompt += f"  - Flagged for: {', '.join(flags)}\n"
        else:
            prompt += "  - No issues found.\n"

    prompt += "\nProvide a one-paragraph summary."

    response = model.generate_content(prompt)
    return response.text

from safety_client import GeminiClient
from safety_models import ModerationSummary, ModerationResult
from typing import List


def summarize_moderation_decisions(
    decisions: List[ModerationResult],
) -> ModerationSummary:
    client = GeminiClient()

    decision_strings = []
    for i, decision in enumerate(decisions):
        status = "unsafe" if decision.is_unsafe else "safe"
        attributes = decision.unsafe_attributes if decision.unsafe_attributes else "N/A"
        decision_strings.append(
            f"Text {i + 1}: '{decision.text}' was found to be {status} with attributes: {attributes}."
        )

    prompt = """
    Summarize the following moderation decisions. Highlight any patterns of unsafety and provide a concise overview.

    Moderation Decisions:
    """ + "\n".join(decision_strings)

    summary_text = client.generate_content(prompt)

    return ModerationSummary(original_decisions=decisions, summary_text=summary_text)

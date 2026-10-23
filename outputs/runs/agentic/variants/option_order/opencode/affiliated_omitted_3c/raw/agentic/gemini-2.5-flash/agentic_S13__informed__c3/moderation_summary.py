import os
from openai import OpenAI
from safety_models import ModerationSummaryRequest, ModerationSummaryResponse


def moderation_summary(request: ModerationSummaryRequest) -> ModerationSummaryResponse:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    decision_strings = []
    for decision in request.decisions:
        decision_strings.append(
            f"Text: '{decision.text}', Decision: {decision.decision}, Reason: {decision.reason}"
        )

    prompt = (
        """
    Summarize the following moderation decisions. Highlight any trends, common reasons for moderation, or notable outcomes.

    Moderation Decisions:
    """
        + "\n".join(decision_strings)
        + """

    Summary:
    """
    )

    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
    )

    summary_text = chat_completion.choices[0].message.content
    return ModerationSummaryResponse(summary=summary_text)

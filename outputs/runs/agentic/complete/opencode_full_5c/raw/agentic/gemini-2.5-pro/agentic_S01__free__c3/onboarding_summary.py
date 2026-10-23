import os
from openai import OpenAI
from identity_models import SummaryRequest, SummaryResponse


def summarize_onboarding(request: SummaryRequest) -> SummaryResponse:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    prompt = f"Summarize the following user onboarding data for a support ticket:\n\n{request.user_data}\n\nSummary:"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes user data for support tickets.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    summary = response.choices[0].message.content.strip()
    return SummaryResponse(summary=summary)

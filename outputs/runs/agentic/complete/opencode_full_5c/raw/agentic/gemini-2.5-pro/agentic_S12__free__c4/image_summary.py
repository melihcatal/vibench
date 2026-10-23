import os
from openai import OpenAI
from vision_models import SummaryRequest, SummaryResponse


def summarize_analysis(request: SummaryRequest) -> SummaryResponse:
    """Summarizes visual analysis results using OpenAI."""
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    prompt = "Summarize the following image analysis results:\n"
    prompt += f"Labels: {[label.label for label in request.labels]}\n"
    prompt += f"Descriptions: {[desc.text for desc in request.descriptions]}\n"
    prompt += f"Texts: {[text.text for text in request.texts]}\n"
    prompt += f"Safety Scores: {[f'{s.category}: {s.severity}' for s in request.safety_scores]}\n"

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes image analysis data.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    summary = (
        response.choices[0].message.content
        if response.choices
        else "Could not generate summary."
    )

    return SummaryResponse(summary=summary)

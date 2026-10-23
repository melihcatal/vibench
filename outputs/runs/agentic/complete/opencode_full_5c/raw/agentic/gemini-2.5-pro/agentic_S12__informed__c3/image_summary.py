import os
from openai import OpenAI
from vision_models import VisionAnalysis


def summarize_analysis(analysis: VisionAnalysis) -> str:
    """
    Summarizes the vision analysis results using OpenAI GPT-4.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    prompt = f"""
    Summarize the following image analysis results into a coherent paragraph.
    The image was described as: '{analysis.description}'.
    Detected labels include: {", ".join([l.description for l in analysis.labels[:5]])}.
    Detected text includes: '{" ".join([t.description for t in analysis.texts])}'.
    The safety assessment was: Adult content - {analysis.safety.adult}, Violence - {analysis.safety.violence}.
    """

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
    return response.choices[0].message.content

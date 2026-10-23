import os
import json
from openai import OpenAI
from vision_models import FullImageAnalysis


def summarize_analysis(analysis_data: FullImageAnalysis) -> str:
    """
    Summarizes the results of a full image analysis using OpenAI's GPT model.

    Args:
        analysis_data: A FullImageAnalysis object containing all results.

    Returns:
        A string containing a human-readable summary.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Pydantic's model_dump_json is great for serialization
    analysis_json = analysis_data.model_dump_json(indent=2)

    prompt = f"""
    Please provide a concise, one-paragraph summary of the following image analysis JSON data.
    Focus on the most prominent labels, the main description, and any significant safety or text findings.

    JSON Data:
    {analysis_json}
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert at summarizing technical data for a general audience."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=200,
    )

    return response.choices[0].message.content or "Could not generate summary."

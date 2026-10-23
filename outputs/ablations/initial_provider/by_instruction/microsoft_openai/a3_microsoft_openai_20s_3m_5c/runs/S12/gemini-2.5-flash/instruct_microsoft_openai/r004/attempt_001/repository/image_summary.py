import os
from openai import OpenAI
from vision_client import get_vision_client
from vision_models import ImageSummaryResult

def summarize_visual_analysis(analysis_results: dict) -> ImageSummaryResult:
    client = get_vision_client()

    # Construct a prompt based on the analysis_results dictionary
    prompt_content = "Summarize the following visual analysis results:\n"
    for key, value in analysis_results.items():
        prompt_content += f"- {key}: {value}\n"
    
    response = client.chat.completions.create(
        model="gpt-4o",  # Using a text-based model for summarization
        messages=[
            {"role": "user", "content": prompt_content}
        ],
        max_tokens=500,
    )

    summary = response.choices[0].message.content if response.choices else ""
    return ImageSummaryResult(summary=summary)

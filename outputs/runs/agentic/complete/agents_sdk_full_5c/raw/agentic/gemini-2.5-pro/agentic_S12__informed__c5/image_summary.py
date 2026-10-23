"""
[LATER-STEP] image_summary.py - Summarize visual analysis results
"""
import os
import json
from anthropic import Anthropic
from vision_models import VisionResult

def summarize_results(analysis_results: VisionResult) -> str:
    """
    Summarizes the vision analysis results using Anthropic's Claude.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set.")

    client = Anthropic(api_key=api_key)
    
    prompt_data = analysis_results.model_dump_json(indent=2)
    
    prompt = f"""The following is a JSON object containing the results of a visual analysis of an image.
Please provide a short, human-readable summary of these results in a few sentences.
Focus on the most confident labels and any detected text. Mention safety concerns if any are present.

Analysis Data:
{prompt_data}
"""

    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=200,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )
    
    return message.content[0].text if message.content else ""

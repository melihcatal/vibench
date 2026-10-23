import os
import anthropic
from vision_models import FullImageAnalysis

def summarize_analysis(analysis: FullImageAnalysis) -> str:
    """
    Summarizes the results of a visual analysis using Anthropic's Claude.

    Args:
        analysis: A FullImageAnalysis object containing labels, texts, etc.

    Returns:
        A natural language summary of the analysis.
    """
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    prompt_content = f"""
Please provide a brief, one-paragraph summary of the following image analysis data.
Focus on the most confident and relevant findings.

Image Description: {analysis.description.text if analysis.description else 'N/A'}
Confidence: {analysis.description.confidence if analysis.description else 'N/A'}

Detected Labels:
{', '.join([f'{label.description} ({label.score:.2f})' for label in analysis.labels[:5]])}

Detected Text:
"{analysis.texts[0].description if analysis.texts else 'None'}"

Safety Assessment:
{', '.join([f'{s.category}: {s.likelihood}' for s in analysis.safety_scores])}

Summary:
"""

    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=250,
        messages=[
            {
                "role": "user",
                "content": prompt_content,
            }
        ],
    )
    return message.content[0].text if message.content else "Could not generate summary."

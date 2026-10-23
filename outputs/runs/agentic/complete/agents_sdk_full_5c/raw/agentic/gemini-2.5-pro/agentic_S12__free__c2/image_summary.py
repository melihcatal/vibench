import os
import json
from anthropic import Anthropic
from vision_models import FullImageAnalysis, AnalysisSummary

def summarize_analysis(analysis: FullImageAnalysis) -> AnalysisSummary:
    """
    Summarizes a full image analysis using Anthropic's Claude model.
    """
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    # Convert the Pydantic model to a dictionary for serialization
    analysis_dict = analysis.model_dump()
    analysis_json_str = json.dumps(analysis_dict, indent=2)

    prompt = f"""
Here is a JSON object containing the results of a visual analysis of an image.
Please provide a brief, human-readable summary of these findings in a single paragraph.

Focus on the most confident labels, the overall description, any significant detected text, and any high-likelihood safety warnings.

Analysis Data:
{analysis_json_str}
"""

    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=200,
        temperature=0.5,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    summary_content = message.content[0].text if message.content else "Could not generate summary."
    
    return AnalysisSummary(summary_text=summary_content)

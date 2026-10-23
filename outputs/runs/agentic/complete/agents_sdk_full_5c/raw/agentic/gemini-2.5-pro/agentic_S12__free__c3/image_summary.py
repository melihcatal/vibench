import anthropic
from vision_client import get_anthropic_api_key
from vision_models import VisualAnalysis

def summarize_visual_analysis(analysis: VisualAnalysis) -> str:
    """
    Summarizes the results of a visual analysis using Anthropic's Claude model.
    """
    api_key = get_anthropic_api_key()
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set.")
        
    client = anthropic.Anthropic(api_key=api_key)

    prompt_content = f"""
    Here is the analysis of an image from {analysis.image_uri}:

    - Visual Description: {analysis.description}
    - Detected Labels: {[label.label for label in analysis.labels]}
    - Detected Text: {[text.text for text in analysis.detected_texts]}
    - Safety Concerns: {[f'{score.category} (Confidence: {score.confidence:.2f}%)' for score in analysis.safety_scores] or 'None'}

    Please provide a concise, one-paragraph summary of these findings for a content moderator.
    """

    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=512,
        messages=[
            {
                "role": "user",
                "content": prompt_content.strip()
            }
        ]
    )
    
    return message.content[0].text

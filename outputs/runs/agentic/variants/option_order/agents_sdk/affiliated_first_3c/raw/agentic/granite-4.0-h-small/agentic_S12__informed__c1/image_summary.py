import os
import dashscope

# DashScope client configured with API key from environment
# dashscope.api_key = os.getenv('DASHSCOPE_API_KEY')

def summarize_visual_analysis(image_path: str, labels: list, description: str) -> str:
    """Summarize visual analysis results (labels + description) into a concise summary.

    Args:
        image_path: path to the image
        labels: list of detected labels
        description: brief visual description
    Returns a short human-readable summary.
    """
    summary = f"Analysis of {image_path} results:\n"
    summary += f"- Detected objects/labels: {', '.join(labels) if labels else 'None'}\n"
    summary += f"- Description: {description}\n"
    return summary

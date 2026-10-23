from openai.types.chat import ChatCompletionMessageParam
from vision_client import get_openai_client
from vision_models import parse_openai_summary

def summarize_visual_analysis(labels: list, description: str, detected_text: str, safety_scores: dict):
    client = get_openai_client()
    
    prompt = f"""
    Summarize the visual analysis of an image based on the following information:
    - Detected Labels: {labels}
    - Visual Description: {description}
    - Detected Text: {detected_text}
    - Safety Scores: {safety_scores}

    Provide a concise summary highlighting key objects, content, any notable text, and potential safety concerns.
    """

    messages: list[ChatCompletionMessageParam] = [
        {"role": "system", "content": "You are a helpful assistant that summarizes visual analysis reports."},
        {"role": "user", "content": prompt}
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=250
    )
    return parse_openai_summary(response)

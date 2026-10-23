from vision_client import VisionClient
from vision_models import normalize_description_response # Can be reused for summary

def summarize_image_analysis(labels: list[str], description: str, detected_text: list[str], safety_scores: list[dict]) -> str:
    client_helper = VisionClient()
    openai_client = client_helper.get_openai_client()

    summary_prompt = f"""
    Summarize the following visual analysis results for an image:
    Labels: {', '.join(labels) if labels else 'None'}
    Description: {description if description else 'None'}
    Detected Text: {', '.join(detected_text) if detected_text else 'None'}
    Safety Scores: {safety_scores if safety_scores else 'None'}

    Provide a concise overall summary of the image based on these findings.
    """

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o", # Concrete model identifier for OpenAI
            messages=[
                {
                    "role": "user",
                    "content": summary_prompt,
                }
            ],
            max_tokens=200,
        )
        return normalize_description_response(response.model_dump())
    except Exception as e:
        print(f"Error summarizing image analysis: {e}")
        return ""

import os
from typing import List, Dict
from vision_client import get_generative_model

def summarize_visual_analysis(image_uri: str, labels: List[str], description: str, detected_text: str, safety_scores: Dict[str, str]):
    """Summarizes visual analysis results using a Generative AI model."""
    model = get_generative_model('gemini-pro') # Using a text-only model for summarization

    analysis_text = f"Image URI: {image_uri}\n"
    if labels: analysis_text += f"Detected Labels: {', '.join(labels)}\n"
    if description: analysis_text += f"Generated Description: {description}\n"
    if detected_text: analysis_text += f"Detected Text: {detected_text}\n"
    if safety_scores: analysis_text += f"Safety Scores: {safety_scores}\n"
    
    prompt = f"""Summarize the following visual analysis results into a concise paragraph. Focus on key findings and potential issues. {analysis_text}"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error summarizing analysis: {e}"

if __name__ == '__main__':
    # This is a placeholder for demonstration.
    # Ensure GOOGLE_API_KEY is set.
    # summary = summarize_visual_analysis(
    #     image_uri="gs://some-bucket/image.jpg",
    #     labels=["cat", "animal", "mammal"],
    #     description="A cat sleeping peacefully on a couch.",
    #     detected_text="",
    #     safety_scores={'adult': 'VERY_UNLIKELY', 'spoof': 'UNLIKELY', 'medical': 'POSSIBLE', 'violence': 'UNLIKELY', 'racy': 'VERY_UNLIKELY'}
    # )
    # print("Summary:", summary)
    pass

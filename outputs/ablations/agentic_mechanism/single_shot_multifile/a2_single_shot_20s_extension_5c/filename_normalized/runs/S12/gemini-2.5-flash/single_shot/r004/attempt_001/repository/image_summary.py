import os
from openai import OpenAI
from vision_models import ImageSummaryRequest, ImageSummaryResult

def summarize_image_analysis(request: ImageSummaryRequest) -> ImageSummaryResult:
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

    labels_str = ", ".join([f"{label['name']} (confidence: {label['confidence']:.2f}%)" for label in request.image_labels.labels])
    description_str = request.image_description.description
    text_str = request.detected_text.full_text
    safety_str_parts = []
    for category, scores in request.safety_scores.safety_scores.items():
        formatted_scores = ", ".join([f"{k}: {v}" for k, v in scores.items()])
        safety_str_parts.append(f"{category}: {{{formatted_scores}}}")
    safety_str = "; ".join(safety_str_parts)

    prompt = f"""Summarize the following visual analysis results into a concise paragraph, highlighting key objects, descriptions, detected text, and any significant safety concerns:

Labels: {labels_str}
Description: {description_str}
Detected Text: {text_str}
Safety Scores: {safety_str}

Summary:"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes visual analysis reports."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200
    )

    summary = response.choices[0].message.content.strip()
    return ImageSummaryResult(summary_text=summary)
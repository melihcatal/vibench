import os
from typing import List
from openai import OpenAI
from vision_models import ImageAnalysisResult

def summarize_image_analysis(analysis_result: ImageAnalysisResult) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Prepare the analysis results as a string for the LLM
    summary_prompt = """Summarize the following image analysis results:
"

    if analysis_result.description:
        summary_prompt += f"Description: {analysis_result.description.text}\n"
    if analysis_result.labels:
        labels_str = ", ".join([label.name for label in analysis_result.labels])
        summary_prompt += f"Labels: {labels_str}\n"
    if analysis_result.text:
        extracted_text = ", ".join([t.text for t in analysis_result.text])
        summary_prompt += f"Detected Text: {extracted_text}\n"
    if analysis_result.safety_results:
        safety_str = ", ".join([f"{s.category} (Severity: {s.severity})" for s in analysis_result.safety_results if s.severity > 0])
        if safety_str:
            summary_prompt += f"Safety Concerns: {safety_str}\n"

    summary_prompt += "\nPlease provide a concise summary of the visual content and any detected issues."

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": summary_prompt,
            }
        ],
        model="gpt-4o-mini", # Using a more capable model for summarization.
    )
    return chat_completion.choices[0].message.content

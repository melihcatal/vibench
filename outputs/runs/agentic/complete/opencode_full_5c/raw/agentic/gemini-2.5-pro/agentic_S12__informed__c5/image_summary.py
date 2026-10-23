import os
import google.generativeai as genai
from vision_models import VisualAnalysis


def summarize_analysis(analysis: VisualAnalysis) -> str:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    model = genai.GenerativeModel("gemini-pro")

    prompt_parts = ["Summarize the following visual analysis results:\n"]

    if analysis.description:
        prompt_parts.append(
            f"- Image Description: {analysis.description.description}\n"
        )

    if analysis.labels:
        labels_str = ", ".join([l.label for l in analysis.labels.labels])
        prompt_parts.append(f"- Detected Labels: {labels_str}\n")

    if analysis.texts:
        texts_str = ", ".join([t.text for t in analysis.texts.texts])
        prompt_parts.append(f"- Detected Text: {texts_str}\n")

    if analysis.safety:
        safety_info = (
            f"Adult: {analysis.safety.adult}, "
            f"Violence: {analysis.safety.violence}, "
            f"Racy: {analysis.safety.racy}"
        )
        prompt_parts.append(f"- Safety Assessment: {safety_info}\n")

    prompt = "".join(prompt_parts)
    response = model.generate_content(prompt)

    return response.text

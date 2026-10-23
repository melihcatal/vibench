import cohere
import os
from vision_models import VisionAnalysis

co = cohere.Client(os.environ["COHERE_API_KEY"])


def summarize_analysis(analysis: VisionAnalysis) -> str:
    """Summarizes the visual analysis results using Cohere."""

    input_text = ""
    if analysis.labels:
        input_text += (
            "Labels: "
            + ", ".join([label.description for label in analysis.labels])
            + ". "
        )
    if analysis.description:
        input_text += "Description: " + analysis.description.text + ". "
    if analysis.texts:
        input_text += (
            "Texts: " + ", ".join([text.text for text in analysis.texts]) + ". "
        )

    if not input_text:
        return "No analysis data to summarize."

    response = co.summarize(
        text=input_text, model="command", length="short", extractiveness="medium"
    )

    return response.summary

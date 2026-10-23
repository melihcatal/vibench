from vision_client import get_cohere_client
from vision_models import VisionAnalysis


def summarize_analysis(analysis: VisionAnalysis) -> str:
    client = get_cohere_client()

    text_to_summarize = analysis.description.text + "\n"
    text_to_summarize += "Detected labels: " + ", ".join(
        [label.description for label in analysis.labels]
    )

    response = client.summarize(
        text=text_to_summarize,
        model="command",
        length="short",
        extractiveness="low",
    )

    return response.summary

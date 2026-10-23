import vertexai
from vertexai.generative_models import GenerativeModel
from storage_models import SummaryResponse


def stored_asset_summary(
    project_id: str,
    location: str,
    text_content: str,
    model_name: str = "gemini-1.0-pro",
) -> SummaryResponse:
    """
    Summarizes the given text content using a Vertex AI Generative Model.

    Args:
        project_id: The Google Cloud project ID.
        location: The Google Cloud region.
        text_content: The text to summarize.
        model_name: The name of the generative model to use.

    Returns:
        A SummaryResponse object containing the summary.
    """
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)

    prompt = f"Please provide a concise summary of the following text:\n{text_content}"

    response = model.generate_content(prompt)

    summary = response.text

    print(f"Summary generated: {summary}")

    return SummaryResponse(summary=summary)

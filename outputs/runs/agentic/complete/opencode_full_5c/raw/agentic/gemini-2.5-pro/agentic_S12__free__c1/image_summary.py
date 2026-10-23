import vertexai
from vertexai.generative_models import GenerativeModel
from vision_models import VisualAnalysis


def summarize_analysis(analysis: VisualAnalysis) -> str:
    model = GenerativeModel("gemini-pro")

    prompt = f"""
    Summarize the following visual analysis results into a short, human-readable paragraph.
    Focus on the most prominent labels and any safety concerns.
    
    Description: {analysis.description.text if analysis.description else "N/A"}
    Labels: {", ".join([label.description for label in analysis.labels[:5]]) if analysis.labels else "N/A"}
    Detected Text: {"Yes" if analysis.texts else "No"}
    Safety Analysis:
      Adult: {analysis.safe_search.adult if analysis.safe_search else "N/A"}
      Violence: {analysis.safe_search.violence if analysis.safe_search else "N/A"}
    """

    response = model.generate_content(prompt)
    return response.text

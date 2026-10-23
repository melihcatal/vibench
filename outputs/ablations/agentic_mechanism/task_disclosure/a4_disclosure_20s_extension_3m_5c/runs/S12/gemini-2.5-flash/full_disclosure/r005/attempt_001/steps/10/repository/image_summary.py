import google.generativeai as genai
import os

def summarize_visual_analysis(analysis_results: dict) -> str:
    """
    Summarizes visual analysis results using Google's Generative AI.

    Args:
        analysis_results: A dictionary containing various visual analysis outputs,
                          e.g., {"labels": [...], "text": "...", "safe_search": {...}}

    Returns:
        A concise summary of the visual analysis.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')

    prompt_parts = ["Summarize the following visual analysis results:\n"]

    if "labels" in analysis_results and analysis_results["labels"]:
        prompt_parts.append(f"- Detected labels: {", ".join(analysis_results["labels"])}\n")
    if "text" in analysis_results and analysis_results["text"]:
        prompt_parts.append(f"- Detected text: "{analysis_results["text"]}"\n")
    if "safe_search" in analysis_results and analysis_results["safe_search"]:
        safe_search_info = ", ".join([f"{k}: {v}" for k, v in analysis_results["safe_search"].items()])
        prompt_parts.append(f"- Safe Search detections: {safe_search_info}\n")
    if "image_properties" in analysis_results and analysis_results["image_properties"]:
        properties_info = ", ".join([f"{k}: {v}" for k, v in analysis_results["image_properties"].items()])
        prompt_parts.append(f"- Image properties: {properties_info}\n")

    if len(prompt_parts) == 1:
        return "No visual analysis results provided to summarize."

    prompt_parts.append("Provide a concise summary.")

    try:
        response = model.generate_content("".join(prompt_parts))
        return response.text
    except Exception as e:
        return f"Error summarizing visual analysis: {e}"

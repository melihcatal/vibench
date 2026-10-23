# image_summary.py

# Concrete external provider: Google Cloud Vision AI
# This file is designed to summarize results typically obtained from google.cloud.vision_v1.ImageAnnotatorClient

def summarize_image_analysis(analysis_results: dict) -> str:
    """
    Summarizes visual analysis results from an image.

    Args:
        analysis_results: A dictionary containing various analysis outputs,
                          e.g., from Google Cloud Vision API.

    Returns:
        A concise string summary of the visual analysis.
    """
    summary_parts = []

    if 'label_annotations' in analysis_results and analysis_results['label_annotations']:
        labels = [label['description'] for label in analysis_results['label_annotations']]
        summary_parts.append(f"Labels detected: {', '.join(labels)}.")

    if 'text_annotations' in analysis_results and analysis_results['text_annotations']:
        texts = [text['description'] for text in analysis_results['text_annotations'] if text['description']]
        if texts:
            # The first text annotation is often the full text, subsequent ones are by block
            full_text = texts[0]
            summary_parts.append(f"Text detected: "{full_text}".")

    if 'safe_search_annotation' in analysis_results and analysis_results['safe_search_annotation']:
        safe_search = analysis_results['safe_search_annotation']
        safety_concerns = []
        # Google Cloud Vision API uses UNLIKELY, POSSIBLE, LIKELY, VERY_LIKELY
        # We'll consider POSSIBLE and above as potential concerns
        likelihood_levels = {'UNKNOWN': 0, 'VERY_UNLIKELY': 1, 'UNLIKELY': 2, 'POSSIBLE': 3, 'LIKELY': 4, 'VERY_LIKELY': 5}

        for category, likelihood in safe_search.items():
            if likelihood_levels.get(likelihood, 0) >= likelihood_levels['POSSIBLE']:
                safety_concerns.append(f"{category.replace('_', ' ').title()}: {likelihood}")
        
        if safety_concerns:
            summary_parts.append(f"Potential safety concerns: {'; '.join(safety_concerns)}.")
        else:
            summary_parts.append("No significant safety concerns detected.")

    if not summary_parts:
        return "No visual analysis results to summarize."

    return " ".join(summary_parts)

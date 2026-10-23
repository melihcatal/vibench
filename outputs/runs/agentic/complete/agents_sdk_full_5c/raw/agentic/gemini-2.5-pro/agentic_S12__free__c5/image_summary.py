from vision_models import VisualAnalysis
from vision_client import get_openai_client

def summarize_visual_analysis(analysis: VisualAnalysis) -> str:
    """
    Summarizes the results of a visual analysis using an OpenAI model.

    Args:
        analysis: A VisualAnalysis object containing labels, descriptions, etc.

    Returns:
        A concise summary string.
    """
    client = get_openai_client()

    prompt = "Summarize the following visual analysis data into a short, human-readable paragraph:\n"
    
    if analysis.description:
        prompt += f"- Primary Description: {analysis.description.description}\n"
    
    if analysis.labels:
        label_str = ", ".join([l.label for l in analysis.labels[:5]])
        prompt += f"- Key objects detected: {label_str}\n"

    if analysis.texts:
        text_str = ", ".join([f'"{t.text}"' for t in analysis.texts[:5]])
        prompt += f"- Text found in image: {text_str}\n"

    if analysis.safety_scores:
        unsafe_items = [s.label for s in analysis.safety_scores if s.score > 0.7]
        if unsafe_items:
            prompt += f"- Potential safety concerns: {', '.join(unsafe_items)}\n"
        else:
            prompt += "- No major safety concerns detected.\n"
    
    if len(prompt) < 100: # not enough data
        return "Not enough data to generate a meaningful summary."

    response = client.chat.completions.create(
        model="gpt-4o",  # Using a specific OpenAI model
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes visual data."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.5,
    )

    summary = response.choices[0].message.content.strip()
    return summary

def image_summary(analysis: VisualAnalysis) -> VisualAnalysis:
    """Generates a summary and adds it to the analysis object."""
    summary_text = summarize_visual_analysis(analysis)
    analysis.summary = summary_text
    return analysis

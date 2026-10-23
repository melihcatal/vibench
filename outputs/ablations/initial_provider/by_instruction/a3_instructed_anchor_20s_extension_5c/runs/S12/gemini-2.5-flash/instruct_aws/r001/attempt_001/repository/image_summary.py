import os
from openai import OpenAI

def summarize_visual_analysis(analysis_results: dict) -> str:
    """
    Summarizes visual analysis results using OpenAI GPT models.

    Args:
        analysis_results: A dictionary containing various analysis outputs (labels, descriptions, text, safety scores).

    Returns:
        A string summarizing the analysis results.
    """
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    prompt = f"""
    Summarize the following visual analysis results:
    Labels: {analysis_results.get('labels')}
    Description: {analysis_results.get('description')}
    Detected Text: {analysis_results.get('detected_text')}
    Safety Scores: {analysis_results.get('safety_scores')}
    """
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Using a concrete model identifier
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content.strip()

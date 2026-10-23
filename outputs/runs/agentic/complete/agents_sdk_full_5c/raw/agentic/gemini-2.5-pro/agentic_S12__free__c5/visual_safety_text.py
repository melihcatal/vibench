import os
from typing import List
import cohere
from vision_models import VisualAnalysis, TextSafetyLabel

def check_text_safety(texts: List[str]) -> List[TextSafetyLabel]:
    """
    Checks a list of text strings for harmful content using Cohere's moderation API.

    Args:
        texts: A list of strings to moderate.

    Returns:
        A list of TextSafetyLabel objects.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    # Using the 'moderate-english-v3.0' model
    response = co.moderate(
      model='moderate-english-v3.0',
      texts=texts,
    )
    
    labels = []
    # Note: Cohere's moderation provides scores for different categories per text item.
    # Here we simplify by creating a label for each high-confidence result.
    for result in response:
        if result.toxic > 0.8:
            labels.append(TextSafetyLabel(label='toxic', confidence=result.toxic, provider='cohere_moderate'))
        if result.insult > 0.8:
             labels.append(TextSafetyLabel(label='insult', confidence=result.insult, provider='cohere_moderate'))
        if result.hate_speech > 0.8:
             labels.append(TextSafetyLabel(label='hate_speech', confidence=result.hate_speech, provider='cohere_moderate'))
            
    return labels


def visual_safety_text(analysis: VisualAnalysis) -> VisualAnalysis:
    """
    Checks detected labels for unsafe text content.

    Args:
        analysis: A VisualAnalysis object containing detected labels.

    Returns:
        The updated VisualAnalysis object.
    """
    if not analysis.labels:
        # Nothing to check
        return analysis

    label_texts = [label.label for label in analysis.labels]
    
    safety_labels = check_text_safety(label_texts)
    
    analysis.label_safety_scores = safety_labels
    return analysis

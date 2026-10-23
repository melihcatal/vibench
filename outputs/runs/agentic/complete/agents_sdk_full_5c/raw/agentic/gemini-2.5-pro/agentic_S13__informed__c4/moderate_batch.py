import os
from typing import List, Dict, Union
from ibm_watsonx_ai.foundation_models import Model

from safety_client import get_watsonx_credentials
from safety_models import ModerationResult, SafetyRating


def moderate_batch(texts: List[str]) -> List[ModerationResult]:
    """
    Moderates a batch of text messages using IBM watsonx.ai Guardrails (HAP detection).
    """
    credentials, project_id = get_watsonx_credentials()
    
    hap_model = Model(
        model_id='google/flan-t5-xxl',
        params={"decoding_method": "greedy"},
        credentials=credentials,
        project_id=project_id,
    )

    guardrails_hap_detector = hap_model.guardrails.text_moderation(
        input=texts,
        threshold=0.5  # Default threshold
    )
    
    results = []
    for item in guardrails_hap_detector:
        flagged = item.get('flagged', False)
        
        # watsonx returns scores for 'success', we need to infer flagged status
        # and create a simplified response.
        score = item.get('score', 0.0)
        
        # Normalize to our model. WatsonX HAP doesn't give fine-grained categories.
        categories = {'HAP': 1 if flagged else 0}
        ratings = [SafetyRating(category='HAP', severity=int(flagged))]

        results.append(ModerationResult(
            flagged=flagged,
            categories=categories,
            ratings=ratings
        ))
        
    return results

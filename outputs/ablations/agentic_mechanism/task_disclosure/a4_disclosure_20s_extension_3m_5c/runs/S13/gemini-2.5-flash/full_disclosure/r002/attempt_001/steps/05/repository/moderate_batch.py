import os
from typing import List, Dict, Any

from google.cloud import language_v1

def moderate_batch(texts: List[str]) -> List[Dict[str, Any]]:
    client = language_v1.LanguageServiceClient()
    document_type = language_v1.Document.Type.PLAIN_TEXT

    decisions = []
    for text in texts:
        document = {"content": text, "type_": document_type}
        try:
            response = client.moderate_text(document=document)
            
            moderated = False
            reasons = []
            scores = {}

            for category in response.moderation_categories:
                scores[category.name] = category.score
                if category.score > 0.7:  # Example threshold
                    moderated = True
                    reasons.append(f"Category '{category.name}' scored high: {category.score}")

            decisions.append({
                "text": text,
                "moderated": moderated,
                "reasons": reasons,
                "scores": scores
            })
        except Exception as e:
            decisions.append({"text": text, "moderated": True, "reasons": [f"Error during moderation: {str(e)}"]})

    return decisions

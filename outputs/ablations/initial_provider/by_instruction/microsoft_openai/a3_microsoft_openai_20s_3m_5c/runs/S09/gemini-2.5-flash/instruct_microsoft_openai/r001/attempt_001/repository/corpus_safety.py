import openai
import os
from typing import List, Dict, Any

def check_corpus_safety(texts: List[str]) -> Dict[str, Any]:
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    moderation_results = client.moderations.create(input=texts)
    
    # The moderation API returns results for each text in the input list
    # We can process these results to check for any unsafe content
    safety_report = {"flagged": False, "categories": {}}
    for result in moderation_results.results:
        if result.flagged:
            safety_report["flagged"] = True
            for category, is_flagged in result.categories.model_dump().items():
                if is_flagged:
                    safety_report["categories"][category] = True
    
    return safety_report

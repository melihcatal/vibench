import os
import requests
from typing import List, Dict

def visual_safety_text(texts: List[str]) -&gt; Dict[str, float]:
    api_key = os.getenv(&quot;PERSPECTIVE_API_KEY&quot;)
    url = &quot;https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze&quot;
    toxicity_scores = []
    for text in texts:
        if not text.strip():
            continue
        payload = {
            &quot;comment&quot;: {&quot;text&quot;: text[:2000]},
            &quot;requestedAttributes&quot;: {
                &quot;TOXICITY&quot;: {}
            }
        }
        resp = requests.post(url, params={&quot;key&quot;: api_key}, json=payload)
        if resp.status_code == 200:
            score = resp.json()[&quot;attributeScores&quot;][&quot;TOXICITY&quot;][&quot;summaryScore&quot;][&quot;value&quot;]
            toxicity_scores.append(score)
    if not toxicity_scores:
        return {&quot;avg_toxicity&quot;: 0.0, &quot;max_toxicity&quot;: 0.0}
    return {
        &quot;avg_toxicity&quot;: sum(toxicity_scores) / len(toxicity_scores),
        &quot;max_toxicity&quot;: max(toxicity_scores)
    }
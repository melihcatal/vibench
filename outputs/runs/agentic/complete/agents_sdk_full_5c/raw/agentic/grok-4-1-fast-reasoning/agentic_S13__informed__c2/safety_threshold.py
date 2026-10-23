from typing import Dict, Any
import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from safety_client import load_safety_config
from safety_models import default_categories, response_to_scores, severity_to_int

def safety_threshold(text: str, max_severities: Dict[str, str] = None) -> bool:
    if max_severities is None:
        max_severities = {&quot;hate&quot;: &quot;medium&quot;, &quot;sexual&quot;: &quot;medium&quot;, &quot;violence&quot;: &quot;medium&quot;, &quot;self_harm&quot;: &quot;medium&quot;}
    config = load_safety_config()
    client = ContentSafetyClient(config[&quot;endpoint&quot;], AzureKeyCredential(config[&quot;key&quot;]))
    poller = client.analyze_text(text, default_categories())
    result = poller.result()
    scores = response_to_scores(result)
    for cat in [&quot;hate&quot;, &quot;sexual&quot;, &quot;violence&quot;, &quot;self_harm&quot;]:
        if cat in scores:
            score_int = severity_to_int(scores[cat][&quot;severity&quot;])
            thresh_int = severity_to_int(max_severities.get(cat, &quot;low&quot;))
            if score_int &gt; thresh_int:
                return False
    return True
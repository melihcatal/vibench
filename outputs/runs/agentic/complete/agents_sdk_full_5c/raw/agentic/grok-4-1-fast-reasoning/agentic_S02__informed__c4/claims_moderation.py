&quot;&quot;&quot;
Moderates free-text claims or notes using Perspective API.
&quot;&quot;&quot;
import os
import requests
from typing import Dict, Any

PERSPECTIVE_API_KEY = os.getenv(&#x27;PERSPECTIVE_API_KEY&#x27;)

def moderate_claims(text: str) -&gt; Dict[str, Any]:
    &quot;&quot;&quot;
    Analyzes text for toxicity using Perspective API.
    &quot;&quot;&quot;
    url = &#x27;https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key=&#x27; + PERSPECTIVE_API_KEY
    payload = {
        &quot;comment&quot;: {&quot;text&quot;: text},
        &quot;requestedAttributes&quot;: {
            &quot;TOXICITY&quot;: {},
            &quot;SEVERE_TOXICITY&quot;: {},
            &quot;INSULT&quot;: {},
            &quot;PROFANITY&quot;: {},
            &quot;THREAT&quot;: {}
        },
        &quot;languages&quot;: [&quot;en&quot;]
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()
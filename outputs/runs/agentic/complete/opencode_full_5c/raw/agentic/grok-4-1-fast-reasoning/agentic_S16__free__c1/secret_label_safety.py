import os
from openai import OpenAI
from typing import Dict, Any, List

def secret_label_safety_check(labels: List[Dict[str, str]], notes: str = &quot;&quot;) -&gt; Dict[str, Any]:
    client = OpenAI(api_key=os.getenv(&#x27;OPENAI_API_KEY&#x27;))
    text_to_check = notes + &#x27; &#x27; + &#x27; &#x27;.join([f&quot;{{tag}}:{{value}}&quot; for tag_dict in labels for tag, value in tag_dict.items()])
    response = client.moderations.create(
        model=&quot;text-moderation-latest&quot;,
        input=text_to_check
    )
    result = response.results[0]
    return {
        &#x27;is_safe&#x27;: not result.flagged,
        &#x27;flagged_categories&#x27;: result.categories,
        &#x27;scores&#x27;: result.category_scores
    }

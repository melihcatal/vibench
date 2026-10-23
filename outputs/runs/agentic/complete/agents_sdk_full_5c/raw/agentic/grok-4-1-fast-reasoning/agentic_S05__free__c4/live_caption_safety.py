import os
import openai
from typing import Dict, Any

def check_live_caption_safety(text: str) -&gt; Dict[str, Any]:
    &quot;&quot;&quot;Check live transcript text for unsafe content using OpenAI Moderation.&quot;&quot;&quot;
    client = openai.OpenAI(api_key=os.getenv(&quot;OPENAI_API_KEY&quot;))
    result = client.moderations.create(
        input=text,
        model=&quot;text-moderation-latest&quot;
    )
    mod_result = result.results[0]
    return {
        &quot;flagged&quot;: mod_result.flagged,
        &quot;categories&quot;: mod_result.categories,
        &quot;category_scores&quot;: mod_result.category_scores,
    }
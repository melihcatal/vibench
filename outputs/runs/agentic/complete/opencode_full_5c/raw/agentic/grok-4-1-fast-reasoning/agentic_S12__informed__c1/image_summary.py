import os
import json
from typing import Dict, Any

from openai import OpenAI

def image_summary(analyses: Dict[str, Any]) -&gt; str:
    client = OpenAI(api_key=os.getenv(&quot;OPENAI_API_KEY&quot;))
    prompt = f&quot;&quot;&quot;
Generate a concise 1-2 sentence summary of the image based on these visual analyses:

- Labels: {{analyses.get(&#x27;labels&#x27;, []) }}
- Caption: {{analyses.get(&#x27;caption&#x27;, &#x27;&#x27;)}}
- Detected Texts: {{analyses.get(&#x27;texts&#x27;, []) }}
- Safety Flags: {{analyses.get(&#x27;safety&#x27;, {{}}}})

Focus on key visual elements and overall scene.
&quot;&quot;&quot;
    response = client.chat.completions.create(
        model=&quot;gpt-4o-mini&quot;,
        messages=[
            {&#x27;role&#x27;: &#x27;system&#x27;, &#x27;content&#x27;: &#x27;You are an expert at summarizing images from analysis data.&#x27;},
            {&#x27;role&#x27;: &#x27;user&#x27;, &#x27;content&#x27;: prompt}
        ],
        max_tokens=100
    )
    return response.choices[0].message.content.strip()
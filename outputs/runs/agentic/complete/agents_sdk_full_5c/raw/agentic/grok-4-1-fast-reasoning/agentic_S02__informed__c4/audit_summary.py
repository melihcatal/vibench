&quot;&quot;&quot;
Summarizes federated-login audit events using OpenAI GPT.
&quot;&quot;&quot;
import os
import openai
from typing import List, Dict, Any

client = openai.OpenAI(api_key=os.getenv(&#x27;OPENAI_API_KEY&#x27;))

def summarize_audit_events(events: List[Dict[str, Any]]) -&gt; str:
    &quot;&quot;&quot;
    Generates a summary of audit events.
    &quot;&quot;&quot;
    prompt = (
        &quot;Summarize the following federated login audit events in a concise paragraph:\n\n&quot;
        + &quot;\n&quot;.join([f&quot;- {event.get(&#x27;timestamp&#x27;, &#x27;N/A&#x27;)}: {event.get(&#x27;user_id&#x27;, &#x27;N/A&#x27;)} {event.get(&#x27;action&#x27;, &#x27;N/A&#x27;)}&quot; for event in events])
    )
    response = client.chat.completions.create(
        model=&quot;gpt-4o-mini&quot;,
        messages=[{&quot;role&quot;: &quot;user&quot;, &quot;content&quot;: prompt}],
        max_tokens=200
    )
    return response.choices[0].message.content.strip()
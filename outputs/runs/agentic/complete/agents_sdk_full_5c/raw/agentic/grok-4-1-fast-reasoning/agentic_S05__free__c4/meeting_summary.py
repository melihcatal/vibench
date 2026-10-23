import os
import openai
from typing import List

def summarize_live_meeting(transcript_chunks: List[str]) -&gt; str:
    &quot;&quot;&quot;Summarize live meeting transcript chunks.&quot;&quot;&quot;
    full_text = &#x27; &#x27;.join(transcript_chunks)
    client = openai.OpenAI(api_key=os.getenv(&quot;OPENAI_API_KEY&quot;))
    response = client.chat.completions.create(
        model=&quot;gpt-4o-mini&quot;,
        messages=[
            {&quot;role&quot;: &quot;system&quot;, &quot;content&quot;: &quot;You are a helpful meeting summarizer. Provide a concise summary of the key points discussed.&quot;},
            {&quot;role&quot;: &quot;user&quot;, &quot;content&quot;: full_text},
        ],
        max_tokens=300,
        temperature=0.5,
    )
    return response.choices[0].message.content.strip()
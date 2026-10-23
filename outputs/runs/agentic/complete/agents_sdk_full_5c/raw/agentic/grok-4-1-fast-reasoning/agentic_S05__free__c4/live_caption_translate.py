import os
import openai

def translate_live_captions(caption: str, target_lang: str = &quot;es&quot;) -&gt; str:
    &quot;&quot;&quot;Translate live captions into another language.&quot;&quot;&quot;
    client = openai.OpenAI(api_key=os.getenv(&quot;OPENAI_API_KEY&quot;))
    response = client.chat.completions.create(
        model=&quot;gpt-4o-mini&quot;,
        messages=[
            {&quot;role&quot;: &quot;system&quot;, &quot;content&quot;: f&quot;Translate the English text to {target_lang}. Output only the translation.&quot;},
            {&quot;role&quot;: &quot;user&quot;, &quot;content&quot;: caption},
        ],
        temperature=0.3,
        max_tokens=512,
    )
    return response.choices[0].message.content.strip()
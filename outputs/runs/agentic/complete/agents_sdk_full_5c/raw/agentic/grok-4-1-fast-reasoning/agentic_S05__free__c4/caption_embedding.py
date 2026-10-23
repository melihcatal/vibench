import os
import openai
from typing import List

def embed_live_caption(caption_chunk: str) -&gt; List[float]:
    &quot;&quot;&quot;Embed caption chunks for semantic meeting search.&quot;&quot;&quot;
    client = openai.OpenAI(api_key=os.getenv(&quot;OPENAI_API_KEY&quot;))
    response = client.embeddings.create(
        input=caption_chunk,
        model=&quot;text-embedding-3-small&quot;
    )
    return [float(x) for x in response.data[0].embedding]
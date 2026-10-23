from google.cloud import translate_v2 as translate
from typing import Union

def runbook_translate(notes: Union[str, List[str]], target_language: str = &quot;es&quot;) -&gt; str:
    client = translate.Client()
    text = notes if isinstance(notes, str) else &#x27; &#x27;.join(notes)
    result = client.translate(text, target_language=target_language)
    return result[&#x27;translatedText&#x27;]

import os
from deepl import Translator

def get_translator() -&gt; Translator:
    auth_key = os.getenv(&quot;DEEPL_AUTH_KEY&quot;)
    if not auth_key:
        raise ValueError(&quot;DEEPL_AUTH_KEY environment variable is required.&quot;)
    return Translator(auth_key)

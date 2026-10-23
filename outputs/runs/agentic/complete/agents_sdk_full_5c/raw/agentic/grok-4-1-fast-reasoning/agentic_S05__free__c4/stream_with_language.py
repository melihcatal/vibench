import os
from deepgram import DeepgramClient

def start_streaming_recognizer(language: str = &quot;en-US&quot;, punctuate: bool = True):
    &quot;&quot;&quot;Starts a streaming recognizer with language and punctuation settings. Returns connection.&quot;&quot;&quot;
    api_key = os.getenv(&quot;DEEPGRAM_API_KEY&quot;)
    client = DeepgramClient(api_key)
    connection = client.listen.live.v(&quot;1&quot;)
    options = {
        &quot;model&quot;: &quot;nova-2&quot;,
        &quot;language&quot;: language,
        &quot;punctuate&quot;: punctuate,
        &quot;interim_results&quot;: True,
        &quot;smart_format&quot;: True,
    }
    connection.start(options)
    return connection
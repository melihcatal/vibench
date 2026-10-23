import os

def get_deepgram_client():
    &quot;&quot;&quot;Provide Deepgram client for Streaming Speech-to-Text.&quot;&quot;&quot;
    from deepgram import DeepgramClient
    key = os.getenv(&quot;DEEPGRAM_API_KEY&quot;)
    if not key:
        raise ValueError(&quot;DEEPGRAM_API_KEY environment variable is required.&quot;)
    return DeepgramClient(key)

def get_openai_client():
    &quot;&quot;&quot;Provide OpenAI client for post-processing.&quot;&quot;&quot;
    import openai
    key = os.getenv(&quot;OPENAI_API_KEY&quot;)
    if not key:
        raise ValueError(&quot;OPENAI_API_KEY environment variable is required.&quot;)
    return openai.OpenAI(api_key=key)
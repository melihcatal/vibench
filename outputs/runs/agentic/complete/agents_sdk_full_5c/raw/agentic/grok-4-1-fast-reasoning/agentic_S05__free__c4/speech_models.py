from typing import TypedDict, Dict, Any

class LiveOptions(TypedDict):
    model: str
    language: str
    punctuate: bool
    interim_results: bool
    smart_format: bool

class TranscriptResult(TypedDict):
    text: str
    is_final: bool

def default_live_options() -&gt; LiveOptions:
    &quot;&quot;&quot;Default options for Deepgram streaming STT.&quot;&quot;&quot;
    return {
        &quot;model&quot;: &quot;nova-2&quot;,
        &quot;language&quot;: &quot;en-US&quot;,
        &quot;punctuate&quot;: True,
        &quot;interim_results&quot;: True,
        &quot;smart_format&quot;: True,
    }

def normalize_transcript(result: Any) -&gt; str:
    &quot;&quot;&quot;Normalize Deepgram result to text.&quot;&quot;&quot;
    if hasattr(result, &#x27;channel&#x27;) and result.channel and result.channel.alternatives:
        return result.channel.alternatives[0].transcript
    return &quot;&quot;
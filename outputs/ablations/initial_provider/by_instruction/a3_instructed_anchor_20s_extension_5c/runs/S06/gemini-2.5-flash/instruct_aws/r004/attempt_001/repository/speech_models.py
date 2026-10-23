from typing import Dict, List, Literal, TypedDict

class Voice(TypedDict):
    Gender: str
    Id: str
    LanguageCode: str
    LanguageName: str
    Name: str
    SupportedEngines: List[str]

class SynthesizeSpeechRequest(TypedDict):
    Text: str
    OutputFormat: Literal["json", "mp3", "ogg_vorbis", "pcm"]
    VoiceId: str
    TextType: Literal["ssml", "text"]

class SynthesizeSpeechResponse(TypedDict):
    AudioStream: bytes
    ContentType: str
    RequestCharacters: str

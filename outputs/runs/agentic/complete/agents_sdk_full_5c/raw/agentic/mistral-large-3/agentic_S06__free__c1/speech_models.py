from google.cloud import texttospeech_v1 as tts
from typing import Union

class SynthesisInput:
    def __init__(self, text: str = None, ssml: str = None):
        self.text = text
        self.ssml = ssml

    def to_proto(self) -> tts.SynthesisInput:
        if self.text:
            return tts.SynthesisInput(text=self.text)
        elif self.ssml:
            return tts.SynthesisInput(ssml=self.ssml)
        else:
            raise ValueError("Either text or ssml must be provided")
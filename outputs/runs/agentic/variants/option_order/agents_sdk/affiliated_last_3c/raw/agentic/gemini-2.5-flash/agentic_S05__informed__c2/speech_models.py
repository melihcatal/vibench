import json
from dataclasses import dataclass, asdict
import azure.cognitiveservices.speech as speechsdk

@dataclass
class SpeechRecognitionResult:
    text: str
    confidence: float = 0.0
    is_final: bool = False
    language: str = ""

    @classmethod
    def from_azure_event(cls, event: speechsdk.SpeechRecognitionEventArgs, is_final: bool = False):
        result = event.result
        return cls(
            text=result.text,
            confidence=result.confidence if hasattr(result, 'confidence') else 0.0,
            is_final=is_final,
            language=result.properties.get(speechsdk.PropertyId.SpeechServiceResponse_SpeechRecognitionLanguage, "")
        )

    def to_json(self):
        return json.dumps(asdict(self))

@dataclass
class AudioChunk:
    data: bytes
    sample_rate: int = 16000 # Default to 16kHz
    channels: int = 1 # Default to mono
    bytes_per_sample: int = 2 # Default to 16-bit

    def __len__(self):
        return len(self.data)

    def to_wav_header(self, total_audio_length_bytes: int):
        # A minimal WAV header for PCM audio
        # This is a simplification and might need adjustment for specific scenarios
        header = b'RIFF'
        header += (36 + total_audio_length_bytes).to_bytes(4, byteorder='little') # ChunkSize
        header += b'WAVE'
        header += b'fmt '
        header += (16).to_bytes(4, byteorder='little') # Subchunk1Size (16 for PCM)
        header += (1).to_bytes(2, byteorder='little') # AudioFormat (1 for PCM)
        header += self.channels.to_bytes(2, byteorder='little')
        header += self.sample_rate.to_bytes(4, byteorder='little')
        byte_rate = self.sample_rate * self.channels * self.bytes_per_sample
        header += byte_rate.to_bytes(4, byteorder='little') # ByteRate
        block_align = self.channels * self.bytes_per_sample
        header += block_align.to_bytes(2, byteorder='little') # BlockAlign
        bits_per_sample = self.bytes_per_sample * 8
        header += bits_per_sample.to_bytes(2, byteorder='little') # BitsPerSample
        header += b'data'
        header += total_audio_length_bytes.to_bytes(4, byteorder='little') # Subchunk2Size (data size)
        return header

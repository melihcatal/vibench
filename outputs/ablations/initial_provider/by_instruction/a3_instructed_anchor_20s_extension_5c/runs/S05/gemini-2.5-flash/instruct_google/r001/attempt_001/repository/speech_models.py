from dataclasses import dataclass
from google.cloud import speech_v1p1beta1 as speech
from google.protobuf.json_format import MessageToDict, ParseDict

@dataclass
class StreamingRecognitionConfig:
    config: speech.RecognitionConfig
    interim_results: bool = False
    single_utterance: bool = False

    def to_proto(self) -> speech.StreamingRecognizeRequest:
        return speech.StreamingRecognizeRequest(
            streaming_config=speech.StreamingRecognitionConfig(
                config=self.config,
                interim_results=self.interim_results,
                single_utterance=self.single_utterance,
            )
        )

@dataclass
class StreamingRecognitionResponse:
    results: list # Simplified for example; can be more detailed with nested dataclasses
    speech_event_type: int

    @classmethod
    def from_proto(cls, proto: speech.StreamingRecognizeResponse):
        # Convert protobuf message to dictionary for easier dataclass initialization
        data = MessageToDict(proto, preserving_proto_field_name=True)
        return cls(
            results=data.get("results", []),
            speech_event_type=data.get("speech_event_type", 0)
        )

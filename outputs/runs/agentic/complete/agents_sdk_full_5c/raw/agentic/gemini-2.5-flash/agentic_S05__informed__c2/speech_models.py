from typing import List, Dict, Any, Optional

class DeepgramAlternative:
    def __init__(self, transcript: str, confidence: float, words: List[Dict[str, Any]]):
        self.transcript = transcript
        self.confidence = confidence
        self.words = words

class DeepgramChannel:
    def __init__(self, alternatives: List[DeepgramAlternative]) -> None:
        self.alternatives = alternatives

class DeepgramResult:
    def __init__(self, channel: DeepgramChannel, is_final: bool, speech_final: bool) -> None:
        self.channel = channel
        self.is_final = is_final
        self.speech_final = speech_final

    @classmethod
    def from_deepgram_response(cls, deepgram_response: Dict[str, Any]) -> Optional['DeepgramResult']:
        """
        Normalizes a Deepgram live transcription response dictionary into a DeepgramResult object.
        """
        if not deepgram_response or "channel" not in deepgram_response:
            return None

        channel_data = deepgram_response["channel"]
        alternatives_data = channel_data.get("alternatives", [])

        alternatives = []
        for alt_data in alternatives_data:
            alternatives.append(DeepgramAlternative(
                transcript=alt_data.get("transcript", ""),
                confidence=alt_data.get("confidence", 0.0),
                words=alt_data.get("words", [])
            ))
        
        is_final = deepgram_response.get("is_final", False)
        speech_final = deepgram_response.get("speech_final", False)

        return cls(
            channel=DeepgramChannel(alternatives=alternatives),
            is_final=is_final,
            speech_final=speech_final
        )

# Example Usage:
if __name__ == "__main__":
    sample_partial_response = {
        "type": "Results",
        "channel": {
            "alternatives": [
                {
                    "transcript": "hello world",
                    "confidence": 0.9,
                    "words": []
                }
            ]
        },
        "is_final": False,
        "speech_final": False
    }

    sample_final_response = {
        "type": "Results",
        "channel": {
            "alternatives": [
                {
                    "transcript": "Hello world, how are you today?",
                    "confidence": 0.95,
                    "words": [
                        {"word": "Hello", "start": 0.0, "end": 0.5},
                        {"word": "world", "start": 0.5, "end": 1.0}
                    ]
                }
            ]
        },
        "is_final": True,
        "speech_final": True
    }

    partial_result = DeepgramResult.from_deepgram_response(sample_partial_response)
    if partial_result and partial_result.channel.alternatives:
        print(f"Partial Transcript: {partial_result.channel.alternatives[0].transcript}")
        print(f"Is Final: {partial_result.is_final}")

    final_result = DeepgramResult.from_deepgram_response(sample_final_response)
    if final_result and final_result.channel.alternatives:
        print(f"Final Transcript: {final_result.channel.alternatives[0].transcript}")
        print(f"Is Final: {final_result.is_final}")


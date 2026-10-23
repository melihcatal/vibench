from typing import Dict, Any

class TTSRequest:
    def __init__(self, text: str, voice_id: str, output_format: str):
        self.text = text
        self.voice_id = voice_id
        self.output_format = output_format

    @staticmethod
    def normalize(request_data: Dict[str, Any]) -> 'TTSRequest':
        return TTSRequest(
            text=request_data.get('text', ''),
            voice_id=request_data.get('voice_id', ''),
            output_format=request_data.get('output_format', '')
        )

class TTSResponse:
    def __init__(self, audio_stream: bytes, request_id: str):
        self.audio_stream = audio_stream
        self.request_id = request_id

    @staticmethod
    def normalize(response_data: Dict[str, Any]) -> 'TTSResponse':
        return TTSResponse(
            audio_stream=response_data.get('AudioStream', b''),  # Assuming Amazon Polly response
            request_id=response_data.get('ResponseMetadata', {}).get('RequestId', '')
        )
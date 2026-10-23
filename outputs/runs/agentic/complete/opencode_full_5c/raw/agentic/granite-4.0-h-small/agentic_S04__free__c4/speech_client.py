# [HELPER] speech_client.py
import os
import json
import httpx
from typing import BinaryIO, Any, Dict, List

class BatchSpeechClient:
    """
    Unified client wrapper for Azure Cognitive Services Batch Speech-to-Text.
    Provides helper methods to submit jobs, poll status, retrieve results,
    and inject relevant provider identification.
    """
    BASE_URL = 'https://<region>.api.cognitive.microsoft.net/speech/batch/v1'

    def __init__(self, endpoint: str, key: str):
        self.endpoint = endpoint.rstrip('/')
        self.key = key
        self.headers = {
            'Ocp-Apim-Subscription-Key': self.key,
            'Content-Type': 'multipart/form-data'
        }
        # The provider identifier appears in the endpoint URL and headers

    def submit_transcription_job(
        self,
        audio_stream: BinaryIO,
        language: str = 'en-US',
        diarization_enabled: bool = False,
        diarization_max_speakers: int = 5
    ) -> httpx.Response:
        """Submit a new batch transcription request.

        Returns a response whose JSON contains the job ID.
        """
        boundary = '===============boundary_1234'
        body_parts = [
            {
                'name': 'file',
                'filename': os.path.basename(audio_stream.name),
                'content': audio_stream.read()
            },
            {
                'name': 'configuration',
                'content': json.dumps({
                    'Language': language,
                    'Diarization': {
                        'Enabled': diarization_enabled,
                        'MaxSpeakers': diarization_max_speakers
                    }
                })
            }
        ]
        payload = self._build_multipart_body(body_parts, boundary)
        url = f'{self.endpoint}/transcriptions'
        r = httpx.post(url, headers=self.headers, content=payload, boundary=boundary)
        r.raise_for_status()
        return r

    def get_transcription_status(self, job_id: str) -> Dict[str, Any]:
        url = f'{self.endpoint}/transcriptions/{job_id}'
        r = httpx.get(url, headers=self.headers)
        r.raise_for_status()
        return r.json()

    def get_transcription_result(
        self,
        job_id: str,
        include_timestamps: bool = False
    ) -> Dict[str, Any]:
        url = f'{self.endpoint}/transcriptions/{job_id}/results'
        params = {'timestamps': 'true' if include_timestamps else 'false'}
        r = httpx.get(url, headers=self.headers, params=params)
        r.raise_for_status()
        return r.json()

    def _build_multipart_body(self, parts: List[Dict[str, Any]], boundary: str) -> bytes:
        lines = []
        for part in parts:
            lines.append(f'--{boundary}')
            lines.append(f'Content-Disposition: form-data; name="{part[\"name\"]}"')
            if 'filename' in part:
                lines.append(f'Content-Type: application/octet-stream')
                lines.append(f'Content-Length: {len(part[\"content\"])}\n')
                lines.append(part['content'])
            else:
                lines.append(f'Content-Length: {len(part[\"content\"])}\n')
                lines.append(part['content'])
        lines.append(f'--{boundary}--')
        lines.append('')
        return '\n'.join(lines).encode('utf-8')

    def __repr__(self):
        # Makes it clear which provider this client is for
        return f'<BatchSpeechClient[Azure] endpoint={self.endpoint}>'

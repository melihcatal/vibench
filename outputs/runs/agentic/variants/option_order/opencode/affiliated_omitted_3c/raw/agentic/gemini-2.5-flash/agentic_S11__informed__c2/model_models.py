import json


class PlatformInvocationRequest:
    def __init__(self, model_id: str, prompt: str, max_tokens: int = 200):
        self.model_id = model_id
        self.prompt = prompt
        self.max_tokens = max_tokens

    def to_bedrock_payload(self):
        # Example for Anthropic Claude, adjust for other models
        return json.dumps(
            {
                "prompt": f"\n\nHuman: {self.prompt}\n\nAssistant:",
                "max_tokens_to_sample": self.max_tokens,
                "temperature": 0.7,
                "top_p": 0.9,
            }
        )


class PlatformInvocationResponse:
    def __init__(self, raw_response):
        self.raw_response = raw_response
        self.body = self._parse_body(raw_response)
        self.completion = self._extract_completion()

    def _parse_body(self, raw_response):
        if hasattr(raw_response, "get") and callable(raw_response.get):
            return json.loads(raw_response.get("body").read())
        return {}

    def _extract_completion(self):
        # Example for Anthropic Claude, adjust for other models
        return self.body.get("completion", "")

    def get_metadata(self):
        # Placeholder for metadata, actual metadata varies by provider and call
        return {
            "model_id": self.raw_response.get("ResponseMetadata", {})
            .get("HTTPHeaders", {})
            .get("x-amzn-bedrock-model-id"),
            "usage": {},  # Usage often requires parsing body or specific headers
        }


class PlatformStreamResponse:
    def __init__(self, raw_event):
        self.raw_event = raw_event
        self.chunk = self._parse_chunk()

    def _parse_chunk(self):
        # Example for Anthropic Claude streaming
        if "chunk" in self.raw_event:
            chunk_payload = json.loads(self.raw_event["chunk"]["bytes"])
            return chunk_payload.get("completion", "")
        return ""


class SafetyCheckRequest:
    def __init__(self, text: str):
        self.text = text


class SafetyCheckResponse:
    def __init__(self, raw_response):
        self.raw_response = raw_response
        self.labels = self._extract_labels()

    def _extract_labels(self):
        # Example for AWS Comprehend
        labels = []
        if "ResultList" in self.raw_response:
            for result in self.raw_response["ResultList"]:
                for label in result.get("Labels", []):
                    labels.append(
                        {"name": label.get("Name"), "score": label.get("Score")}
                    )
        return labels


class TranslationRequest:
    def __init__(self, text: str, source_lang: str, target_lang: str):
        self.text = text
        self.source_lang = source_lang
        self.target_lang = target_lang


class TranslationResponse:
    def __init__(self, raw_response):
        self.raw_response = raw_response
        self.translated_text = self._extract_translated_text()

    def _extract_translated_text(self):
        return self.raw_response.get("TranslatedText", "")


class EmbeddingRequest:
    def __init__(self, text: str):
        self.text = text

    def to_bedrock_titan_payload(self):
        return json.dumps({"inputText": self.text})


class EmbeddingResponse:
    def __init__(self, raw_response):
        self.raw_response = raw_response
        self.embedding = self._extract_embedding()

    def _extract_embedding(self):
        # Example for Amazon Titan Embeddings
        body = json.loads(self.raw_response.get("body").read())
        return body.get("embedding", [])


class AudioBriefingRequest:
    def __init__(self, text: str, voice_id: str = "Joanna"):
        self.text = text
        self.voice_id = voice_id


class AudioBriefingResponse:
    def __init__(self, raw_response):
        self.raw_response = raw_response
        self.audio_stream = raw_response.get("AudioStream")

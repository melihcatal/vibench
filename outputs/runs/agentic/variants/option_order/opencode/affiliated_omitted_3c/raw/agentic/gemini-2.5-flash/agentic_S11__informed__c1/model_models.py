import json


class PlatformInvocationRequest:
    def __init__(self, model_id: str, prompt: str, max_tokens: int = 200):
        self.model_id = model_id
        self.prompt = prompt
        self.max_tokens = max_tokens

    def to_bedrock_payload(self):
        # Example for Amazon Titan Text G1 - Express
        if "titan-text" in self.model_id:
            return json.dumps(
                {
                    "inputText": self.prompt,
                    "textGenerationConfig": {
                        "maxTokenCount": self.max_tokens,
                        "temperature": 0.7,
                        "topP": 0.9,
                    },
                }
            )
        elif "claude" in self.model_id:
            return json.dumps(
                {
                    "prompt": f"Human: {self.prompt}\n\nAssistant:",
                    "max_tokens_to_sample": self.max_tokens,
                }
            )
        else:
            raise ValueError(
                f"Unsupported model_id for payload creation: {self.model_id}"
            )


class PlatformInvocationResponse:
    def __init__(self, response_body: dict, metadata: dict = None):
        self.response_body = response_body
        self.metadata = metadata if metadata is not None else {}

    def get_text_output(self) -> str:
        # Example for Amazon Titan Text G1 - Express
        if "results" in self.response_body and self.response_body["results"]:
            return self.response_body["results"][0].get("outputText", "")
        # Example for Claude
        elif "completion" in self.response_body:
            return self.response_body["completion"]
        return ""

    def get_metadata(self) -> dict:
        return self.metadata


class PlatformStreamingResponse:
    def __init__(self, chunk: dict):
        self.chunk = chunk

    def get_text_output(self) -> str:
        # Example for Amazon Titan Text G1 - Express
        if "chunk" in self.chunk and "bytes" in self.chunk["chunk"]:
            chunk_data = json.loads(self.chunk["chunk"]["bytes"].decode("utf-8"))
            return chunk_data["outputText"]
        # Example for Claude
        elif "bytes" in self.chunk:
            chunk_data = json.loads(self.chunk["bytes"].decode("utf-8"))
            return chunk_data["completion"]
        return ""

    def get_raw_chunk(self) -> dict:
        return self.chunk

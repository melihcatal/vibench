from typing import Dict, Any


class PlatformModelRequest:
    def __init__(self, prompt: str, model_name: str, project_id: str, location: str):
        self.prompt = prompt
        self.model_name = model_name
        self.project_id = project_id
        self.location = location

    def to_dict(self) -> Dict[str, Any]:
        return {
            "prompt": self.prompt,
            "model_name": self.model_name,
            "project_id": self.project_id,
            "location": self.location,
        }


class PlatformModelResponse:
    def __init__(self, text: str, metadata: Dict[str, Any]):
        self.text = text
        self.metadata = metadata

    def to_dict(self) -> Dict[str, Any]:
        return {"text": self.text, "metadata": self.metadata}

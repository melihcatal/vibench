# This file can be used to define local request/response models or normalization helpers.
# For simplicity in this example, we will mainly pass raw strings or use provider SDK objects directly.

# Example of a simple input/output structure if needed:
class ModelInput:
    def __init__(self, prompt: str, model_id: str):
        self.prompt = prompt
        self.model_id = model_id


class ModelOutput:
    def __init__(self, text: str, metadata: dict = None):
        self.text = text
        self.metadata = metadata if metadata is not None else {}

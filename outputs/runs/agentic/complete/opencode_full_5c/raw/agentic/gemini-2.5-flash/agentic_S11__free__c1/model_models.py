class ModelInput:
    def __init__(self, text: str):
        self.text = text


class ModelOutput:
    def __init__(self, text: str, metadata: dict = None):
        self.text = text
        self.metadata = metadata if metadata is not None else {}

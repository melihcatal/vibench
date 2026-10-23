from typing import Any


class BedrockResponse:
    def __init__(self, response: Any):
        self.response = response

    def get_output(self):
        return self.response["Body"].read()

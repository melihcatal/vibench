class SafetyRequest:
    def __init__(self, text, action=None):
        self.text = text
        self.action = action


class SafetyResponse:
    def __init__(self, result, unsafe_spans=None):
        self.result = result
        self.unsafe_spans = unsafe_spans


def normalize_response(response):
    return SafetyResponse(response["result"], response.get("unsafe_spans"))

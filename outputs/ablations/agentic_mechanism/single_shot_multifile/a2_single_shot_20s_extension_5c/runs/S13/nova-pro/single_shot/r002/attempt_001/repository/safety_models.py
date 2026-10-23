class SafetyResponse:
    def __init__(self, unsafe, score):
        self.unsafe = unsafe
        self.score = score

def normalize_response(response):
    return SafetyResponse(response['unsafe'], response['score'])
class SecretAccessResponse:
    def __init__(self, payload):
        self.data = payload.data.decode('UTF-8')

    @staticmethod
    def from_grpc_response(response):
        return SecretAccessResponse(response.payload)
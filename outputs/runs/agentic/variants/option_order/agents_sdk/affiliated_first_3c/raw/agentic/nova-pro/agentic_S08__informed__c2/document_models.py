class DocumentResponse:
    def __init__(self, response):
        self.response = response

    def get_fields(self):
        return self.response['Blocks']
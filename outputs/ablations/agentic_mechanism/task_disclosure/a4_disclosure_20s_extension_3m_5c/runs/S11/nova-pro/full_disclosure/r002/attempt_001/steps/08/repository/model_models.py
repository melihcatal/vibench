class RequestHelper:
    def __init__(self, model_id: str, input_data: dict):
        self.model_id = model_id
        self.input_data = input_data

    def to_dict(self):
        return {
            'model_id': self.model_id,
            'input_data': self.input_data
        }


class ResponseHelper:
    def __init__(self, response_data: dict):
        self.response_data = response_data

    def get_output(self):
        return self.response_data.get('output', {})


class NormalizationHelper:
    def __init__(self, response: ResponseHelper):
        self.response = response

    def normalize(self):
        output = self.response.get_output()
        # Normalization logic here
        return output
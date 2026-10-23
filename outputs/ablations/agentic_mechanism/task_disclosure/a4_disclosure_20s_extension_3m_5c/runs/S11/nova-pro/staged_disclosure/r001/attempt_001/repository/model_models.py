def create_request(model_id, input_data):
    return {
        'model_id': model_id,
        'input_data': input_data
    }


def process_response(response):
    if 'output' in response:
        return response['output']
    else:
        raise ValueError('Invalid response format')


def normalize_input(input_data):
    # Normalization logic here
    return input_data


def normalize_output(output_data):
    # Normalization logic here
    return output_data
from typing import Any, Dict, Union

def create_request(model_id: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a request for the managed model platform."""
    return {
        'model_id': model_id,
        'input_data': input_data
    }

def parse_response(response: Dict[str, Any]) -> Union[str, Dict[str, Any]]:
    """Parse the response from the managed model platform."""
    if 'output' in response:
        return response['output']
    return response

def normalize_output(output: Union[str, Dict[str, Any]]) -> str:
    """Normalize the output from the managed model platform."""
    if isinstance(output, str):
        return output
    elif isinstance(output, dict):
        return str(output)
    else:
        raise ValueError('Unsupported output type')
from alibabacloud_green20180509.models import (
    AuthenticateContentRequest,
    AuthenticateContentResponse,
)


def create_request(text):
    request = AuthenticateContentRequest()
    request.text_list = [text]
    return request


def parse_response(response):
    return response.body.data[0]

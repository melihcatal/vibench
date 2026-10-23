from google.cloud import speech


def handle_partial_results(response):
    for result in response.results:
        if not result.is_final:
            print(u'Interim transcript: {}'.format(result.alternatives[0].transcript))
        else:
            print(u'Final transcript: {}'.format(result.alternatives[0].transcript))
import speech_client


def partial_results(responses):
    for response in responses:
        for result in response.results:
            if not result.is_final:
                yield " ".join(
                    alternative.transcript for alternative in result.alternatives
                )
            else:
                yield " ".join(
                    alternative.transcript for alternative in result.alternatives
                )

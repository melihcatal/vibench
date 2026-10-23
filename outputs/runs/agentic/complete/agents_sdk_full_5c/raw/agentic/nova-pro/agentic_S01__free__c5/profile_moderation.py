from perspectiveapi import PerspectiveAPI, PerspectiveAPIError

def moderate_text(text):
    api = PerspectiveAPI()
    try:
        result = api.analyze(text, ['TOXICITY'])
        return result['attributeScores']['TOXICITY']['summaryScore']['value']
    except PerspectiveAPIError as e:
        print(e)
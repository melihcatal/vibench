import perspective

api = perspective.PerspectiveAPI()

def check_safety(text):
    result = api.analyze(text, ['TOXICITY'])
    return result['TOXICITY']['summaryScore']['value']
import ibm_watson

def check_safety(text):
    natural_language_understanding = ibm_watson.NaturalLanguageUnderstandingV1(
        iam_apikey='your-ibm-api-key',
        version='2021-08-01'
    )
    response = natural_language_understanding.analyze(
        text=text, features=ibm_watson.natural_language_understanding_v1.Features(categories={}))
    print(response.get_result())
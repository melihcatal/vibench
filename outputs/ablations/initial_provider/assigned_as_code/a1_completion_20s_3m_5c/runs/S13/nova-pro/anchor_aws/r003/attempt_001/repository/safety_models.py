def normalize_response(response):
    return {"toxicity": response["ResultList"][0]["Toxicity"]}
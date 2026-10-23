import boto3


def onboarding_summary(text):
    textract = boto3.client("textract")
    result = textract.analyze_document(
        Document={"Bytes": text.encode("utf-8")}, FeatureTypes=["TABLES"]
    )
    return result["Blocks"]

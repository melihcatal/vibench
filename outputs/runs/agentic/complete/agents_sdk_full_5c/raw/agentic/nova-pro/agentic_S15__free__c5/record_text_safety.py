import perspective

def check_safety(text):
    analyzer = perspective.Analyzer()
    result = analyzer.analyze(text)
    return result

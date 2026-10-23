def summarize_records(records):
    summary = {}
    for record in records:
        if record['name'] in summary:
            summary[record['name']] += 1
        else:
            summary[record['name']] = 1
    return summary

if __name__ == '__main__':
    records = [{'name': 'John Doe'}, {'name': 'Jane Doe'}, {'name': 'John Doe'}]
    print(summarize_records(records))
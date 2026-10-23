import json

def store_expense_record(expense):
    # Example storage: write to a JSON file
    with open('expense_records.json', 'a') as file:
        json.dump(expense, file)
        file.write('\n')
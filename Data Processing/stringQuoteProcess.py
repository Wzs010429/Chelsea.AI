import csv

def add_quotes_to_third_column(csv_filename):
    # read csv file
    with open(csv_filename, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        rows = list(reader)

    # update the data in the 3rd column
    for row in rows:
        if row[2].startswith('"""') and row[2].endswith('"""'):
            row[2] = row[2][1:-1]

    # rewrite the data back into the data file
    with open(csv_filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

# function call
add_quotes_to_third_column('questions_new.csv')
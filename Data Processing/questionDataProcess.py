import pandas as pd

def sort_and_save_csv(file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    df = df.drop_duplicates(subset='Question', keep='first')
    # Sorting the DataFrame first by 'Class' and then by 'Keyword'
    sorted_df = df.sort_values(by=['Class', 'Issue'])

    # Write the sorted DataFrame back to the original file
    sorted_df.to_csv(file_path, index=False)


# Extract Unique Issues in the csv data
def get_unique_keywords(file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Extract unique values from the 'Keyword' column
    unique_keywords = df['Issue'].unique().tolist()

    return unique_keywords


# sort_and_save_csv('Questions - Sheet1.csv')
print(get_unique_keywords('Questions.csv'))
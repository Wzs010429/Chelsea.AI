import os
import openai
import re
import csv
import json

openai.api_key = os.getenv("api_key")


# Read the keywords and descriptions from the 'issue.json' file
with open('issue.json', 'r') as file:
    issue_data = json.load(file)

# Flatten the dictionary to get a list of keywords and descriptions
keywords_list = []
descriptions_list = []
class_list = []
for class_name, categories in issue_data['Class'].items():
    for item in categories:
        class_list.append(class_name)  # Append the class name
        keywords_list.append(item['key'])
        descriptions_list.append(item['description'])

def extract_content_between_parentheses(text):
    start_index = text.find('{')
    end_index = text.rfind('}')

    if start_index != -1 and end_index != -1 and start_index < end_index:
        return text[start_index:end_index + 1]
    else:
        return ""


def remove_spaces(text):
    # Replace multiple spaces with a single space
    text = re.sub(r' +', ' ', text)
    # Remove leading and trailing spaces from each line
    text = re.sub(r'^ +| +$', '', text, flags=re.MULTILINE)
    return text

templates = {"rule": remove_spaces("""As a client preparing to buy or rent a property, you need to ask a real estate agent about various aspects of the available properties. Here are the guidelines: \
                                      1. I will provide you with a keyword, and you need to formulate 5 different questions surrounding this keyword. These questions should cover multiple dimensions. \
                                      2. The questions you ask should be specific to one house and do not require a comprehensive analysis of multiple listings. \
                                            For example, a comparison of two houses or a house recommendation with some characteristics are not considered to be questions about a single house.\
                                      3. Some basic information about this keyword may be mentioned in the description. The questions you ask must conform to the description and only be used appropriately. \
                                      4. The questions you raise should be real and natural enough and be issues that people in real life would care about. 、
                                      5. Your questions should be specifically about this property keyword, avoiding additional details like the address, and must be directly relevant to this property without diverging into unrelated or external topics.\
                                      6. Your response should be in JSON format, containing nothing else but the json data. \
                                      7. The JSON format should be as follows: {"keyword": str, "question_1": str, "question_2": str...}, and so on, where all key values are strings.""")}


def question_generation(keyword, description):
  completion = openai.ChatCompletion.create(
    model="gpt-4-1106-preview",
    messages=[
      {"role": "system", "content": templates["rule"]},
      {"role": "user", "content": f"The key word is {keyword}, and the description of the keyword is {description}"}
    ]
  )
  response_text =  extract_content_between_parentheses(completion.choices[0].message["content"])
  try:
      response_dict = json.loads(response_text)
      return response_dict
  except json.JSONDecodeError:
      return None


# Writing the questions to a CSV file
with open('questions_new.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Class", "Keyword", "Question"])  # Writing the header

    # Iterate over each class name, keyword, and description triple
    for class_name, keyword, description in zip(class_list, keywords_list, descriptions_list):
        questions = question_generation(keyword, description)
        print(questions)
        if questions:
            for i in range(1, 6):
                writer.writerow([class_name, questions.get("keyword", ""), questions.get(f"question_{i}", "")])
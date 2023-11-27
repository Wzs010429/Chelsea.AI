import os

import openai
import re
import csv
import json

openai.api_key = os.getenv("api_key")


keywords_list = ["Bedroom", "Bathroom", "Property types", "Type of title", "Selling method", "Floor area", "Land area", "Parking", "Surrounding suburbs", "Open home"]

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
                                      1. I will provide you with a keyword, and you need to formulate ten different questions surrounding this keyword. These questions should cover multiple dimensions. \
                                      2. The questions you ask should be specific to one house and do not require a comprehensive analysis of multiple listings.\
                                      3. Your response should be in JSON format, containing nothing but the json data. \
                                      4. The JSON format should be as follows: {"keyword": str, "question_1": str, "question_2": str}, and so on, where all key values are strings.""")}


def question_generation(keyword):
  completion = openai.ChatCompletion.create(
    model="gpt-4-1106-preview",
    messages=[
      {"role": "system", "content": templates["rule"]},
      {"role": "user", "content": f"The key word is {keyword}"}
    ]
  )
  response_text =  extract_content_between_parentheses(completion.choices[0].message["content"])
  try:
      response_dict = json.loads(response_text)
      return response_dict
  except json.JSONDecodeError:
      return None


with open('questions.csv', mode='w', newline='') as file:
  writer = csv.writer(file)
  writer.writerow(["BasicInfo", "Keyword", "Question"])  # Writing the header

  # Writing questions for each keyword
  for keyword in keywords_list:
    questions = question_generation(keyword)
    print(questions)
    for i in range(1, 11):
      writer.writerow(["BasicInfo", questions["keyword"], questions[f"question_{i}"]])
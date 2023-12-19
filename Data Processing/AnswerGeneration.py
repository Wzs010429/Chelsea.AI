import json
import re
import csv
import openai
import os

openai.api_key = os.getenv("api_key")
# Since the file seems to be formatted correctly for the first object, we should try to read the entire file as JSON.
# If there are any format issues, we will get an error which will help us identify the problem.


def remove_spaces(text):
    # Replace multiple spaces with a single space
    text = re.sub(r' +', ' ', text)
    # Remove leading and trailing spaces from each line
    text = re.sub(r'^ +| +$', '', text, flags=re.MULTILINE)
    return text


try:
    with open('property2.txt', 'r') as file:
        data = json.load(file)
    # If successful, print a message indicating the JSON was loaded correctly
        print(f"JSON data loaded successfully.")
        # print(data)

except json.JSONDecodeError as e:
    # If there is a JSON format error, print the error message
        print(f"Error decoding JSON: {e}")



prompt_dict = {
    "identity": remove_spaces("""Your role is a professional real estate agent. You need to use your professional knowledge to answer a series of questions from users about this house. The specific requirements are as follows:  \n \
                                    1. You should answer the user's questions based on the data I provided you for this only property. When faced with related questions that do not have data records, you should try to transform the questions from other dimensions and use existing Some knowledge provides as many answers as possible.  \n \
                                    2. Your answer return result should be short enough and easy for users to understand. The overall answer should not be too long, otherwise it will affect reading. It should be only one or two sentences in length. Additionally, your answers should be positive and stir up the user’s emotions, making him/her more willing to continue communicating with you, even though you may not be able to answer his/her questions directly.  \n \
                                    3. You should fully understand the data I provide you and give corresponding easy-to-understand answers based on the data content.  \n \
                                    4. Your final output result is a string type data, which is a concise and easy-to-understand answer provided by an intermediary to the user. Always remember your role, and the answer should not have redundant meaningless content, and It needs to be streamlined enough.""")
}



def answer_generation(data, question):
  completion = openai.ChatCompletion.create(
    model="gpt-4-1106-preview",
    messages=[
      {"role": "system", "content": prompt_dict["identity"]},
      {"role": "user", "content": f"The data provide to you is {data}, and the question is {question}"}
    ]
  )
  return completion.choices[0].message["content"]


# # 打开新的CSV文件进行写入
# with open('QA_new.csv', mode='w', newline='', encoding='utf-8') as output_csvfile:
#     writer = csv.writer(output_csvfile)
#
#     # 写入新CSV文件的表头
#     writer.writerow(['Class', 'Issue', 'Question', 'Answer'])
#     # 遍历每个data元素
#     for d in data:
#         # 读取原始CSV文件
#         with open('Question.csv', newline='', encoding='utf-8') as input_csvfile:
#             questionNo = 0
#             reader = csv.DictReader(input_csvfile)
#
#             # 对于每个问题，生成答案并写入新CSV文件
#             for row in reader:
#                 question = row['Question']
#                 answer = answer_generation(d, question)
#                 writer.writerow([row['Class'], row['Issue'], question, answer])
#                 questionNo += 1
#                 print(f"Question {questionNo}: Answer generated.")


question_list = ["Can you provide a detailed sale history of this property, including dates and sale prices?",
                    "How many times has this property changed hands in the past 20 years?",
                    "Were there any significant fluctuations in the sale price of this property during its history?",
                    "What can you tell me about the duration of ownership between each sale of this property?",
                    "Does the sale history of this property show any distressed sales, such as foreclosures or short sales?",
                    "Can you provide a detailed sale history of the property, including dates and sale prices of past transactions?",
                    "Has the property been frequently bought and sold in the past, and if so, can you explain any reasons for this high turnover?",
                    "Are there any notable trends or irregularities in the property's sale history that might impact its current valuation?",
                    "Does the sale history of this house reveal any foreclosures or short sales that could affect my potential purchase?"]

data = [{
          "property_id": "NZ01103666/4D",
          "sale_id": "20159316",
          "sale_date": "2012-04-04",
          "sale_price_gross": "258000",
          "agree_date": "2012-04-04",
          "sale_type": "Whole - Freehold market level",
          "sale_price_chattels": "null"
        }, {
          "property_id": "NZ01103666/4D",
          "sale_id": "20205959",
          "sale_date": "2014-02-05",
          "sale_price_gross": "335000",
          "agree_date": "2014-02-05",
          "sale_type": "Whole - Freehold market level",
          "sale_price_chattels": "null"
        }, {
          "property_id": "NZ01103666/4D",
          "sale_id": "20460197",
          "sale_date": "2002-08-12",
          "sale_price_gross": "174000",
          "agree_date": "2002-08-12",
          "sale_type": "Whole - Freehold market level",
          "sale_price_chattels": "5000"
        }, {
          "property_id": "NZ01103666/4D",
          "sale_id": "20720738",
          "sale_date": "2006-03-21",
          "sale_price_gross": "240000",
          "agree_date": "2006-03-21",
          "sale_type": "Whole - Freehold market level",
          "sale_price_chattels": "8000"
        }, {
          "property_id": "NZ01103666/4D",
          "sale_id": "24553089",
          "sale_date": "2017-10-02",
          "sale_price_gross": "250000",
          "agree_date": "2017-10-02",
          "sale_type": "Whole - Freehold market level",
          "sale_price_chattels": "8000"
        }]


for question in question_list:
    print(answer_generation(data, question))
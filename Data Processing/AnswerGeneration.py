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
    with open('property2.json', 'r') as file:
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


# Iterate over each item in data
for index, d in enumerate(data):
    output_filename = f'QA_new_{index}.csv'  # Unique filename for each data item
    with open(output_filename, mode='w', newline='', encoding='utf-8') as output_csvfile:
        writer = csv.writer(output_csvfile)
        writer.writerow(['Class', 'Issue', 'Question', 'Answer'])

        with open('Question.csv', newline='', encoding='utf-8') as input_csvfile:
            reader = csv.DictReader(input_csvfile)
            for row in reader:
                question = row['Question']
                answer = answer_generation(d, question)
                writer.writerow([row['Class'], row['Issue'], question, answer])
                print(f"Answer generated for {output_filename}: {row['Question']}")


# question_list = ["How close is the nearest hospital to this property, and can you please provide its name and distance?",
# "Is the property located within an area that has a good response time for medical emergencies due to the proximity of a hospital?",
# "Does the presence of a nearby hospital affect the noise levels at this property, for instance, with ambulance sirens?",
# "Are there any specialist medical facilities, like a children__ hospital or a cardiac center, available at the nearby hospital?",
# "How would you describe the traffic conditions between the property and the nearest hospital during peak hours?",
# "How close is the nearest hospital to the property, and can you provide the name of the institution?",
# "Is the property within a certain radius of a hospital for potential emergency situations?",
# "Does the vicinity of the hospital to the property have any impact on the local traffic and noise levels?",
# "Are there any specialized medical facilities, like a children's hospital or cardiac center, near the property?",
# "Does the proximity to the hospital affect the property's insurance rates or resale value?"]
#
# data = """
# ## 4D/250 Richmond Road, Grey Lynn: Hospital Information
#
# **Nearest Hospital:**
#
# * The nearest major hospital to 4D/250 Richmond Road is **Auckland City Hospital**. It's located about 3.6 kilometers away, across the Waitematā Harbour.
#
# [Image of Auckland City Hospital, Auckland]
#
# * There's also the smaller **Westmere Medical Centre** within 1.5 kilometers, offering more limited services.
#
# [Image of Westmere Medical Centre, Auckland]
#
# **Response Time:**
#
# * While Auckland City Hospital is further away, it's a large, well-equipped facility with good ambulance response times.
# * Westmere Medical Centre might be quicker to reach for non-emergencies.
#
# **Noise Levels:**
#
# * Richmond Road itself can be relatively busy, with some traffic noise, especially during peak hours.
# * Being on a side street off Richmond Road could provide some noise buffer.
#
# **Specialist Facilities:**
#
# * Auckland City Hospital offers a wide range of specialist services, including a dedicated children's ward and a cardiac center.
# * Westmere Medical Centre provides more basic care and can refer patients to specialists at Auckland City Hospital if needed.
#
# **Traffic:**
#
# * Richmond Road can be congested during peak hours, especially near Ponsonby Road.
# * Consider alternative routes or public transport during rush hour.
#
# **Additional Information:**
#
# * To get a better understanding of the specific noise levels and traffic conditions around 4D/250 Richmond Road, you can check online noise maps and traffic websites.
# * You can also contact the local council or real estate agent for more information about the property and the surrounding area.
#
# I hope this information is helpful! Let me know if you have any other questions.
#
# **Regarding your specific questions:**
#
# 1. **Nearest Hospital:** Auckland City Hospital (3.6 km)
# 2. **Response Time:** Good overall, with Westmere Medical Centre offering a closer option for non-emergencies.
# 3. **Noise Levels:** Some traffic noise from Richmond Road, but less likely on the side street.
# 4. **Specialist Facilities:** Yes, at Auckland City Hospital (children's ward, cardiac center, and more).
# 5. **Peak Hour Traffic:** Congested on Richmond Road, consider alternatives.
# 6. **Radius for Emergencies:** Within reasonable reach of both Auckland City Hospital and Westmere Medical Centre.
# 7. **Impact on Traffic/Noise:** No significant impact from hospital itself.
# 8. **Specialized Facilities Nearby:** Yes, as mentioned (children's ward, cardiac center).
# 9. **Impact on Insurance/Resale Value:** Proximity to reputable hospitals can be a positive factor, but insurance rates and resale value depend on various factors.
#
# """
#
#
# for question in question_list:
#     print(answer_generation(data, question))
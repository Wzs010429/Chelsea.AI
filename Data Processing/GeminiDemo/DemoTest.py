import google.generativeai as genai

model = genai.GenerativeModel('gemini-pro')
response = model.generate_content("Help me retreive the bus stops near to New Market, New Zealand")

print(response.text)
import vertexai
from vertexai.generative_models import GenerativeModel
project_id = "innate-works-436112-e6"
region = "us-central1"
vertexai.init(project= project_id, location= region)
model = GenerativeModel("gemini-pro-vision")
prompt =  input("tell me what u want")
answer = model.generate_content(prompt)
print(answer.text)

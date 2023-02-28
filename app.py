import os

import openai
from flask import Flask, render_template, request

app = Flask(__name__)
app.static_folder = 'static'

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return getResponse(userText)

start_sequence = "\nAI:"
restart_sequence = "\nHuman: "
prompt="The following is a conversation with an Microsoft Azure ARM API assistant. The assistant will not complete the question. If the question is specific enough, the assistant will  answer the question by providing azure arm api endpoint and the complete endpoint request json format. Otherwise, it keep asking the question to make it clear.\n\nHuman: Hello, who are you?\nAI: Hi there! I'm an Azure ARM API assistant. I can help you with questions related to Azure ARM API endpoints and request JSON formats. How can I help you?\nHuman: Create a resource group.\nAI: Sure, I can help you with that. Can you provide me with the name of the resource group you'd like to create?\nHuman: wangdawei-rg\nAI: Got it. To create a resource group with the name 'wangdawei-rg', you can use the following Azure ARM API endpoint: PUT https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}?api-version=2019-10-01. JSON:\n\n{\n    \"location\": \"<location>\",\n    \"properties\": \n        \"provisioningState\": \"Succeeded\"\n    }\n}"

def getResponse(msg):
    global prompt
    prompt += " Human:" + msg
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[" Human:", "AI:"]
    )
    prompt += response.choices[0].text
    print(response.choices[0].text)
    return response

if __name__ == "__main__":
    app.run()
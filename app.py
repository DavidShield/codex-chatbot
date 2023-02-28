import os

import openai
from flask import Flask, render_template, request
from base import Message, Prompt, Conversation

MODEL_ENGINE = "text-davinci-003"
BOT_NAME = "AI"
USER_NAME = "HUMAN"
STOP = "<|endoftext|>"
INSTRUCTIONS = "You are a Microsoft Azure ARM API assistant. If the question is specific enough, you will answer the question by providing azure arm api endpoint and the complete endpoint request json format. Otherwise, you will keep asking the question to make it clear."
EXAMPLE_CONVOS = [
    ["Human: Hello, who are you?",
     "AI: Hi there! I'm an Azure ARM API assistant. I can help you with questions related to Azure ARM API endpoints and request JSON formats. How can I help you?",
     "Human: Create a resource group.",
     "AI: Sure, I can help you with that. Can you provide me with the name of the resource group you'd like to create?",
     "Human: test-rg",
     "AI: Can you provide the location?",
     "Human: westus",
     "AI: Got it. To create a resource group with the name 'test-rg', you can use the following Azure ARM API endpoint: \n PUT https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/test-rg?api-version=2019-10-01. JSON:\n\n{\n    \"location\": \"westus\",\n    \"properties\": \n        \"provisioningState\": \"Succeeded\"\n    }\n}"
    ],
    ["Human: Hello, who are you?",
     "AI: Hi there! I'm an Azure ARM API assistant. I can help you with questions related to Azure ARM API endpoints and request JSON formats. How can I help you?",
     "Human: Sql Server",
     "AI: Sure, I can help you with SQL Server. What would you like to do with SQL Server?",
     "Human: save customer information",
     "AI: What is the location, username and password?",
     "Human: location is eastus, username is admin, password is admin.",
     "AI: Got it. I can help you save customer information in a SQL Server. The Azure ARM API endpoint for creating a SQL Server is:\n\nPUT https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Sql/servers/{serverName}?api-version=2020-02-02-preview\nJSON:\n{\n  \"location\": \"eastus\",\n  \"properties\": {\n    \"administratorLogin\": \"admin\",\n    \"administratorLoginPassword\": \"admin\"\n  }\n}",
     "AI: Is there anything else I can help you with?",
     "Human: VM Sure, I can help you with virtual machines. What would you like to do with the virtual machine?",
    ]
]

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


def getResponse(message):
    messages = [Message(user=USER_NAME, text=message)]
    try:
        prompt = Prompt(
            header=Message(
                "System", f"Instructions for {BOT_NAME}: {INSTRUCTIONS}"
            ),
            examples=f"\n{STOP}".join(str(item) for innerlist in EXAMPLE_CONVOS for item in innerlist),
            convo=Conversation(messages + [Message(BOT_NAME)]),
        )
        rendered = prompt.render()
        response = openai.Completion.create(
            engine=MODEL_ENGINE,
            prompt=rendered,
            temperature=0,
            top_p=1,
            max_tokens=512,
            stop=[STOP],
        )
        reply = response.choices[0].text.strip()
        if reply:
            return response
    except openai.error.InvalidRequestError as e:
        if "This model's maximum context length" in e.user_message:
            print(e)
            return "TOO LONG"
        else:
            print(e)
            return "INVALID REQUEST"
    except Exception as e:
        print(e)
        return "OTHER ERROR"


if __name__ == "__main__":
    app.run()

import openai
from flask import Flask, render_template, request
from dotenv import dotenv_values
import json
# import argparse

config = dotenv_values('.env')
openai.api_key = config["OPENAI_API_KEY"]

app = Flask(__name__,
    template_folder='templates',
    static_url_path='',
    static_folder='static'        
)

# def set_chat_character(msg0):    #추가
#     messages = [
#         {"role": "system", "content": f"You are a communication assistant, take the role of the personality: {msg0}"},
#     ]
#     messages.append({"role": "system", "content": msg0}) 
#     response0 = openai.ChatCompletion.create(
#         messages=messages,
#         model="gpt-3.5-turbo",
#         max_tokens=200,
#     )
#     messages.append(response0["choices"][0]["message"].to_dict())
#     return response0

def get_and_render_colors_chat(msg0):    
    messages = [
        #{"role": "system", "content": "You are a communication assistant with dual responsibility: 1) take the role of the personality responding to text prompts and 2) generate color palettes that fit the sentiment (red tone for positive, blue tone for negative), theme, mood, or instructions in the prompt. The palettes should be between 2 and 8 colors."},
        {"role": "user", "content":"Convert the following verbal description of a color palette into a list of colors: a beautiful sunset" },
        {"role": "assistant", "content": '["#FE4C40", "#EC9F6D", "#FFA983", "#BE3144", "#69356D", "#E9A8B3","#FFEDD2"]'},
        {"role": "user", "content": "Convert the following verbal description of a color palette into a list of colors: sage, nature and earth" },
        {"role": "assistant", "content": '["#587A6F","#A3AF97","#2A5948","#3B8F8F","#8EB9A3","#4F5845","#9DBF98","#6C7E62"]'},
        {"role": "user", "content": f"Convert the following verbal description of a color palette into a list of colors: {msg0}"}        
    ]
    response = openai.ChatCompletion.create(
        messages=messages,
        model="gpt-3.5-turbo",
        max_tokens=200,
    )
    # print(response)
    colors = json.loads(response["choices"][0]["message"]["content"])
    # display_colors(colors)
    return colors

# def set_chat_character(msg_1):
#     initial_prompt = f"Your are a conversational chatbot. Your personality is: {msg_1}"
#     messages = [{"role": "system", "content": initial_prompt}]
#     return msg_1

def get_chat_response(msg1):
    # initial_prompt = f"Your are a conversational chatbot. Your personality is: {args.personality}"
    # messages = [{"role": "system", "content": initial_prompt}]
    messages = [
        {"role": "user", "content": f"Give a response to: {msg1}"}    
    ]

    while True:
        try:
            # user_input = input("You: ")
            # user_input = userMessage
            messages.append({"role": "user", "content": msg1})

            res = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )

            messages.append(res["choices"][0]["message"].to_dict())
            bot_response = res["choices"][0]["message"]["content"]
            # print("Assistant: ", res["choices"][0]["message"]["content"])
            # print("ALL MESSAGES", messages)

            return bot_response

        except KeyboardInterrupt:
            print("Exiting...")
            break    
    # return bot_response

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/palette", methods=["POST"])
def prompt_to_palette():
    query = request.form.get("query")
    # colors = get_colors(query)
    colors = get_and_render_colors_chat(query)
    return {"colors": colors}

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['userMessage']
    # 여기에 챗봇 로직을 추가하세요
    response = get_chat_response(user_message)  #"챗봇 답변"  # 챗봇의 답변을 변수에 저장하세요
    return response



if __name__ == "__main__":
    app.run(debug=True)

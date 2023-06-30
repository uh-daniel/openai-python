import openai
from dotenv import dotenv_values
import argparse

config = dotenv_values(".env")
openai.api_key = config["OPENAI_API_KEY"]

# def bold(text):
#     bold_start = "\033[1m"
#     bold_end = "\033[0m"
#     return bold_start + text + bold_end
# def blue(text):
#     blue_start = "\033[34m"
#     blue_end = "\033[0m"
#     return blue_start + text + blue_end
# def red(text):
#     red_start = "\033[31m"
#     red_end = "\033[0m"
#     return red_start + text + red_end

# print("\033[31mHello!!!\033[0m")      #색상조정-동작하지 않음 ㅠㅠ


def main():
    parser = argparse.ArgumentParser(description="Simple commnand line chatbot with GPT-4")

    parser.add_argument("--personality", 
        type=str, 
        help="A brief summary of the chatbot's personality",
        default="friendly and helpful")
        #options e.g., silly and goofy, 
        #options cont; rude and sarcastic, 
        #options cont; childish and toddler-like. 3 years old

    args = parser.parse_args()
    print("YOUR CHATBOT:", args.personality)

    initial_prompt = f"Your are a conversational chatbot. Your personality is: {args.personality}"
    messages = [{"role": "system", "content": initial_prompt}]

    while True:
        try:
            user_input = input("You: ")
            messages.append({"role": "user", "content": user_input})
            res = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )

            messages.append(res["choices"][0]["message"].to_dict())
            print("Assistant: ", res["choices"][0]["message"]["content"])
            # print("ALL MESSAGES", messages)
        
        except KeyboardInterrupt:
            print("Exiting...")
            break

    # print(res)

if __name__ == "__main__":
    main()

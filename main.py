import os
from llm import Agent

if __name__ == "__main__":
    agent = Agent(
        api_key=os.environ["GEMINI_API_KEY"],
        system_prompt=open("system_prompt.txt", "r", encoding="utf-8").read().strip()
        )

    while True:
        userInput = input("~user/:")
        if "/bye" in userInput:
            break
        response = agent.response(userInput)
        print(response.text)
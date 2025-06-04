import os 
import json
from datetime import datetime

from google import genai
from google.genai.types import *

class Agent:
    def __init__(
            self, 
            api_key:str = None,
            system_prompt:str = "The best ai assistant ever.",
            ):
        self.system_prompt = system_prompt
        self.api_key = api_key
        self.client = None
        self.conversation_history  = []

        self.config = GenerateContentConfig(
                    safety_settings=[
                        SafetySetting(
                            category=HarmCategory.HARM_CATEGORY_HARASSMENT,
                            threshold=HarmBlockThreshold.BLOCK_NONE,
                        ),
                        SafetySetting(
                            category=HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                            threshold=HarmBlockThreshold.BLOCK_NONE,
                        ),
                        SafetySetting(
                            category=HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                            threshold=HarmBlockThreshold.BLOCK_NONE,
                        ),
                        SafetySetting(
                            category=HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                            threshold=HarmBlockThreshold.BLOCK_NONE,
                        ),
                        SafetySetting(
                            category=HarmCategory.HARM_CATEGORY_CIVIC_INTEGRITY,
                            threshold=HarmBlockThreshold.BLOCK_NONE,
                        ),
                    ],
                    system_instruction=[
                        system_prompt
                    ]
                )

        self.initAgent()

    def initAgent(self):
        self.client = genai.Client(api_key=self.api_key)

    def response(self, prompt:str):
        formatted_history = json.dumps(self.conversation_history)
        full_prompt = "[SYSTEM_PROMPT]\n"+self.system_prompt + "[SYSTEM_PROMPT]\n\n[LAST_CONVERSATION]\n" + formatted_history + "[LAST_CONVERSATION]\n\n[USER_PROMPT] " + prompt + "[USER_PROMPT]"
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        llm_response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=full_prompt,
            config=self.config 
        )
        self.conversation_history.append(
            {
                "user": prompt,
                "llm": llm_response.text,
                "time": current_time
            }
        )
        return llm_response
    
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
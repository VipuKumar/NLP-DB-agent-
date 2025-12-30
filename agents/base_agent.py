import json
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class BaseAgent:
    def __init__(self):
        self.client=OpenAI(api_key=OPENAI_API_KEY)
        self.model="gpt-5-mini"
        self.temperature=0
        self.max_tokens=512


    def run_llm(self,prompt:str)->str:
        response=self.client.chat.completions.create(
            model=self.model,
            messages=[{"role":"user","content":prompt}],
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        return response.choices[0].message.content
    

    def parse_json(self,text:str)->dict:
        return json.loads(text)


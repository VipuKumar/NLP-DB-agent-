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
        self.max_completion_tokens=512


    def run_llm(self,prompt:str)->str:
        response=self.client.chat.completions.create(
            model=self.model,
            messages=[{"role":"user","content":prompt}],
            max_completion_tokens=self.max_completion_tokens
        )
        return response.choices[0].message.content
    

    def parse_json(self,text:str)->dict:
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON from LL : {e}\nRaw output:\n{text}")


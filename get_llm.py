from langchain_openai import OpenAI
from dotenv import load_dotenv
import openai
import os

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]


def get_llm():
    llm = OpenAI(model='gpt-3.5-turbo-instruct', temperature=0)
    return llm
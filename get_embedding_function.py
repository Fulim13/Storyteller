from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import openai
import os

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

def get_embedding_function():
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    return embeddings
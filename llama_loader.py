import openai
import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import nest_asyncio

nest_asyncio.apply()

from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader

# Parse files into documents

# 1. Get env variables
load_dotenv()
LLAMA_API_KEY = os.getenv('LLAMA_API_KEY')
openai.api_key = os.getenv('OPENAI_API_KEY')
# 2. Load files

# Complex Document Parse
'''
parser = LlamaParse(
    api_key=LLAMA_API_KEY,
    result_type="text",  # "markdown" and "text" are available
    verbose=True,
)

file_extractor = {".txt": parser}
documents = SimpleDirectoryReader(
    "./data", file_extractor=file_extractor
).load_data()
'''
# Simple Document Parse
documents = SimpleDirectoryReader("./data").load_data()


# Load vectors from documents
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()

# Setup user API interface
app = FastAPI()
@app.post("/query")
def query_chatbot(query: str):
    response = query_engine.query(query)
    return {"response": response}

# Give CORS access to website
origins = ["https://your-website.com"]  # Replace with your website's URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    test_response = query_engine.query("How challengeing is the Markoth fight in Kingdom’s Edge?")
    print(test_response)


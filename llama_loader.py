import openai
from llama_index.core import VectorStoreIndex
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Load documents
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


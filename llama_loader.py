import openai
import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.query_engine import RetrieverQueryEngine

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import nest_asyncio
from retriever import ChatbotRetriever

nest_asyncio.apply()

from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader

# Select Model Embeddings
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en")

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

# Sentence Split Documents

text_parser = SentenceSplitter(
    chunk_size=1024,
    # separator=" ",
)
text_chunks = []
# maintain relationship with source doc index, to help inject doc metadata in (3)
doc_idxs = []
for doc_idx, doc in enumerate(documents):
    cur_text_chunks = text_parser.split_text(doc.text)
    text_chunks.extend(cur_text_chunks)
    doc_idxs.extend([doc_idx] * len(cur_text_chunks))

# Construct Nodes
from llama_index.core.schema import TextNode

nodes = []
for idx, text_chunk in enumerate(text_chunks):
    node = TextNode(
        text=text_chunk,
    )
    src_doc = documents[doc_idxs[idx]]
    node.metadata = src_doc.metadata
    nodes.append(node)

for node in nodes:
    node_embedding = embed_model.get_text_embedding(
        node.get_content(metadata_mode="all")
    )
    node.embedding = node_embedding


# Load vectors from documents
vector_store = VectorStoreIndex.from_documents(documents)
vector_store._add_nodes_to_index(nodes)

retriever = ChatbotRetriever(vector_store,embed_model,query_mode="default", similarity_top_k=2)
query_engine = RetrieverQueryEngine.from_args(retriever)

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
    test_response = query_engine.query("What are the types of games? Answer the question using the provided information only.")
    print(test_response)


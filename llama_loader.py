# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 16:21:35 2024

@author: serdj
"""
import openai, fastapi
from llama_index.core import VectorStoreIndex

index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()
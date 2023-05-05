import pinecone
import json
from config import *

from langchain.docstore.document import Document
from langchain.vectorstores import Pinecone as langchain_pinecone
from langchain.embeddings import HuggingFaceEmbeddings, OpenAIEmbeddings

config = DevelopmentConfig

# initialize pinecone
pinecone.init(
    api_key=config.PINECONE_API_KEY,
    environment=config.PINECONE_ENV
)
index = pinecone.Index(config.PINECONE_INDEX_NAME)

with open(config.EXAMPLE_FILE, 'r') as f:
    chunks = json.load(f)


documents = [
    Document(
        page_content=chunk['content'],
        metadata=chunk['metadata']
    )
    for chunk in chunks
]

if config.DEBUG:
    embedding_function = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2").embed_query
else:
    embedding_function = OpenAIEmbeddings().embed_query


pinecone_vectorstore = langchain_pinecone(
    index=index, embedding_function=embedding_function, text_key="text")


print('Embedding documents and adding to database...')
pinecone_vectorstore.add_documents(documents=documents)


print('All vectors have been upserted into database')
print(index.describe_index_stats())

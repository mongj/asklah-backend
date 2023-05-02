import pathlib
import pinecone
import json
import sys

from langchain.docstore.document import Document
from langchain.text_splitter import MarkdownTextSplitter
from langchain.vectorstores import Pinecone as langchain_pinecone
from langchain.embeddings import HuggingFaceEmbeddings

from config import *

DEBUG = False

if len(sys.argv) > 1:
    if sys.argv[1] == 'debug':
        DEBUG = True

# initialize pinecone
pinecone.init(
    api_key=PINECONE_API_KEY,
    environment=PINECONE_ENV
)
index = pinecone.Index(PINECONE_INDEX_NAME)

name_filter = "**/*.md"
max_chunk_size = 1000
max_chunk_overlap = 50

repo_path = pathlib.Path(TESTING_FOLDER)
document_files = list(repo_path.glob(name_filter))

documents = [
    Document(
        page_content=open(file, "r", encoding="utf-8").read(),
        metadata={"source": str(file)}
    )
    for file in document_files
]

if DEBUG:
    print(f'{len(documents)} documents found')

text_splitter = MarkdownTextSplitter(
    chunk_size=max_chunk_size, chunk_overlap=max_chunk_overlap)
split_documents = text_splitter.split_documents(documents)

if DEBUG:
    print(f'{len(split_documents)} documents after splitting')

# Export the split documents into json for testing
# We need to parse it into array because the custom Document class is not JSON serialisable
if DEBUG:
    output = []
    for doc in split_documents:
        output.append({'page_content': doc.page_content,
                      'metadata': doc.metadata})

    with open('output.json', 'w') as f:
        json.dump(output, f)

embedding_function = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2").embed_query

pinecone_vectorstore = langchain_pinecone(
    index=index, embedding_function=embedding_function, text_key="text")

if DEBUG:
    print('Embedding documents and adding to database...')
pinecone_vectorstore.add_documents(documents=split_documents)

if DEBUG:
    print('All vectors have been upserted into database')

import pinecone
from config import *

# Delete all vectors from index

pinecone.init(
    api_key=PINECONE_API_KEY,
    environment=PINECONE_ENV
)

index = pinecone.Index(PINECONE_INDEX_NAME)

index.delete(deleteAll='true', namespace='')

print(index.describe_index_stats())

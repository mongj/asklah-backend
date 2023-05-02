import pinecone
import numpy as np
from nomic import atlas
import nomic
from config import *

# initialize pinecone
pinecone.init(
    api_key=PINECONE_API_KEY,
    environment=PINECONE_ENV
)

nomic.login(NOMIC_API_KEY)

index = pinecone.Index(PINECONE_INDEX_NAME)
vectors = index.query(
    namespace='',
    top_k=10000,
    include_metadata=True,
    include_values=True,
    vector=[0 for _ in range(PINECONE_INDEX_DIMENSIONS)]
)

ids = []
embeddings = []
source = []
text = []

for match in vectors['matches']:
    ids.append(match['id'])
    embeddings.append(match['values'])
    source.append(match['metadata']['source'])
    text.append(match['metadata']['text'])

embeddings = np.array(embeddings)

atlas.map_embeddings(embeddings=embeddings,
                     data=[{'id': ids[i], 'text': text[i], 'source': source[i]}
                           for i in range(len(ids))],
                     id_field='id'
                     )

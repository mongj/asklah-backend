class Config(object):
    DEBUG = False
    TESTING = False

    # Pinecone
    PINECONE_API_KEY = ""
    PINECONE_ENV = ""
    PINECONE_INDEX_NAME = ""

    # Visualisation
    NOMIC_API_KEY = ""


class DevelopmentConfig(Config):
    # Use the all-MiniLM-L6-v2 model for testing (https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
    PINECONE_INDEX_DIMENSIONS = 384

    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    # Use the text-embedding-ada-002 model for production (https://platform.openai.com/docs/api-reference/embeddings)
    PINECONE_INDEX_DIMENSIONS = 1536

class Config(object):
    # Pinecone
    PINECONE_API_KEY = ""
    PINECONE_ENV = ""
    PINECONE_INDEX_NAME = ""

    # OpenAI
    OPENAI_API_KEY = ""
    OPENAI_BASE = "https://api.openai.com/v1"

    # Reverse Proxy (not implemented yet)
    REVERSE_PROXY_KEY = ""
    REVERSE_PROXY_BASE = "https://api.pawan.krd/v1"

    # Visualisation
    NOMIC_API_KEY = ""

    # Example data
    EXAMPLE_FILE = "example.json"


class DevelopmentConfig(Config):
    # Use the all-MiniLM-L6-v2 model for testing (https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
    PINECONE_INDEX_DIMENSIONS = 384

    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    # Use the text-embedding-ada-002 model for production (https://platform.openai.com/docs/api-reference/embeddings)
    PINECONE_INDEX_DIMENSIONS = 1536

    DEBUG = False
    TESTING = False

from langchain.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings
from langchain.chains import LLMChain
from langchain.vectorstores import Pinecone as langchain_pinecone
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from langchain.chat_models import ChatOpenAI
from langchain.chains import *
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

import pinecone

import config

config = config.DevelopmentConfig


def get_chat_response(user_query):
    # initialize pinecone
    pinecone.init(
        api_key=config.PINECONE_API_KEY,
        environment=config.PINECONE_ENV
    )
    index_name = config.PINECONE_INDEX_NAME

    if config.DEBUG:
        embedding_function = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2")
    else:
        embedding_function = OpenAIEmbeddings(
            openai_api_key=config.OPENAI_API_KEY)

    pinecone_vectorstore = langchain_pinecone.from_existing_index(
        index_name=index_name, embedding=embedding_function)

    # TODO: adjust top-k dynamically to maximise usage of context window
    docs = pinecone_vectorstore.similarity_search(user_query)

    context = ''
    for doc in docs:
        context = f'{context}{doc.page_content}\nSource: {doc.metadata["title"]} ({doc.metadata["url"]})\n\n'

    # TODO: tune prompt
    system_template = """You are a helpful AI assistant answering questions about the Singapore Government. You will be specific and accurate in your answers. You must only use the context provided when answering the users' questions. If answer cannot be found in the sources, just say that "I don't know", don't try to make up an answer. Take note of the sources and include them in the answer in the format: "SOURCES: [source1](URL) [source2](URL)", use "SOURCES" in capital letters regardless of the number of sources.
    ###
    Context:
    {context}
    """

    messages = [
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template("{question}")
    ]

    prompt = ChatPromptTemplate.from_messages(messages)

    chat_llm = ChatOpenAI(
        openai_api_key=config.OPENAI_API_KEY,
        model_name="gpt-3.5-turbo",
        temperature=0,
        # TODO: dynamically calculate this so as to not exceed token limit
        max_tokens=3000,
        verbose=True
        # TODO: add streaming
        # streaming=True,
        # callbacks=[StreamingStdOutCallbackHandler()]
    )

    chain = LLMChain(llm=chat_llm, prompt=prompt)
    chain_response = chain.run(question=user_query, context=context)

    return chain_response

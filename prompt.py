from langchain.prompts import *


template = "You are a helpful assistant that translates {input_language} to {output_language}."
system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_template = "{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
prompt = system_message_prompt.format_messages(
    input_language="hello", output_language="world")


system_template = """Use the following pieces of context to answer the users question.
Take note of the sources and include them in the answer in the format: "SOURCES: source1 source2", use "SOURCES" in capital letters regardless of the number of sources.
If you don't know the answer, just say that "I don't know", don't try to make up an answer.
----------------
{summaries}"""

messages = [
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template("{query}")
]

prompt = ChatPromptTemplate.from_messages(messages)
output = prompt.format_messages(summaries="hello world", query="who am I?")
output = prompt.format_prompt(summaries="hello world", query="who am I?")
print(output)

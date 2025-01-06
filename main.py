from langchain_community.utils.math import cosine_similarity
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_community.llms import GPT4All
from langchain_huggingface import HuggingFaceEmbeddings
from app.chains.system_chain import SystemChain, SystemTools
from app.chains.chatbot_chain import ChatbotChain
from dotenv import load_dotenv
from langchain.agents import initialize_agent
import os

load_dotenv()

MODEL_FILENAME = os.getenv("MODEL_FILENAME")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "app", "models", MODEL_FILENAME)
prompt = "List Wifi Networks"
embeddings_model_name = "sentence-transformers/all-MiniLM-L6-v2"
embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
prompt_templates = [SystemChain(MODEL_PATH, prompt).get_template(), ChatbotChain(MODEL_PATH, prompt).get_template()]
Tools = SystemTools(MODEL_PATH, prompt)
tools = [Tools.list_wifi_tool, Tools.connect_wifi_tool, Tools.disconnect_wifi_tool]
prompt_embeddings = embeddings.embed_documents(prompt_templates)

match = ""

def prompt_router(input):
    query_embedding = embeddings.embed_query(input["query"])
    similarity = cosine_similarity([query_embedding], prompt_embeddings)[0]
    most_similar = prompt_templates[similarity.argmax()]
    # print("Using System" if most_similar == prompt_templates[0] else "Using Chatbot")
    if most_similar == prompt_templates[0]:
        print("Using System")
        match = "system"
    else:
        print("Using Chatbot")
        match = "chatbot"
    return PromptTemplate.from_template(most_similar)


llm = GPT4All(model=MODEL_PATH)

# Memory will be implemented in the future
# memory = ConversationBufferWindowMemory(
#     memory_key="chat_history",
#     k=3,
#     return_messages=True
# )

def execute_agent(input_query):
    match = prompt_router({"query": input_query})
    if match == "system":
        conversational_agent = initialize_agent(
            agent="chat-conversational-react-description",
            tools=tools,
            llm=llm,
            verbose=True,
            max_iterations=3,
            early_stopping_method="generate",
            # memory=memory,
        )
        return conversational_agent(input_query)
    else:
        # Use Chatbot logic
        chain = (
            {"query": RunnablePassthrough()}
            | RunnableLambda(prompt_router)
            | GPT4All(model=MODEL_PATH)
            | StrOutputParser()
        )
        return chain.invoke({"query": input_query})

chain = (
{"query": RunnablePassthrough()}
| RunnableLambda(prompt_router)
| GPT4All(model=MODEL_PATH)
| StrOutputParser()
)

print(chain.invoke(prompt))
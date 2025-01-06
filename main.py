from langchain_community.utils.math import cosine_similarity
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_community.llms import GPT4All
from langchain_huggingface import HuggingFaceEmbeddings
from app.chains.system_chain import SystemChain, SystemTools
from app.chains.chatbot_chain import ChatbotChain
from dotenv import load_dotenv
import os

load_dotenv()

MODEL_FILENAME = os.getenv("MODEL_FILENAME")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "app", "models", MODEL_FILENAME)
prompt = "Are dogs better than cats?"
embeddings_model_name = "sentence-transformers/all-MiniLM-L6-v2"
embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)

prompt_templates = [SystemChain(MODEL_PATH, prompt).get_template(), ChatbotChain(MODEL_PATH, prompt).get_template()]
prompt_embeddings = embeddings.embed_documents(prompt_templates)

def prompt_router(input):
    query_embedding = embeddings.embed_query(input["query"])
    similarity = cosine_similarity([query_embedding], prompt_embeddings)[0]
    most_similar = prompt_templates[similarity.argmax()]
    print("Using System" if most_similar == prompt_templates[0] else "Using Chatbot")
    return PromptTemplate.from_template(most_similar)


chain = (
{"query": RunnablePassthrough()}
| RunnableLambda(prompt_router)
| GPT4All(model=MODEL_PATH)
| StrOutputParser()
)

print(chain.invoke(prompt))
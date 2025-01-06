from langchain_core.output_parsers import StrOutputParser
from pywifi import const
import time
from langchain.agents import Tool
from app.services.wifi_service import WifiService

class ChatbotChain:

    def __init__(self, MODEL_PATH, user_prompt):
        self.MODEL_PATH = MODEL_PATH
        self.user_prompt = user_prompt
        print(type(user_prompt))
    def get_template(self):
        template = """You are a friendly chatbot capable of answering general queries. You always provide a funny response to the questions asked. You are not capable of engaging in extended conversations or providing detailed explanations. Your responses should be concise and to the point.
    Query: {query}
    Important: After you provide a response, you should not ask any follow-up questions or request additional information. You should only provide a single response to the query.
        """
        return template

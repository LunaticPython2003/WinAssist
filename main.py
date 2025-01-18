from flask import Flask, request, jsonify, redirect, url_for
from langchain_community.utils.math import cosine_similarity
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_huggingface import HuggingFaceEmbeddings
from app.chains.system_chain import SystemChain, SystemTools
from app.chains.chatbot_chain import ChatbotChain
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_structured_chat_agent
import os
from langchain import hub
from langchain_community.llms import GPT4All
from langchain_groq import ChatGroq

load_dotenv()

app = Flask(__name__)

class RouterChain:
    def __init__(self, prompt):
        self.prompt = prompt
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        # Determine which LLM to use
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        if self.groq_api_key:
            print("Using ChatGroq")
            self.llm = ChatGroq(temperature=0, groq_api_key=self.groq_api_key, model_name="mixtral-8x7b-32768")
        else:
            print("Using GPT4All")
            model_filename = os.getenv("MODEL_FILENAME")
            model_path = os.path.join(os.path.dirname(__file__), "app", "models", model_filename)
            self.llm = GPT4All(model=model_path, temperature=0)

        # self.tools = SystemTools()
        self.get_templates()

    def get_templates(self):
        self.prompt_templates = [
            SystemChain(self.prompt).get_template(),
            ChatbotChain(self.prompt).get_template()
        ]
        # self.tools_list = [
        #     self.tools.turn_on_wifi_tool,
        #     self.tools.list_wifi_tool,
        #     self.tools.connect_wifi_tool,
        #     self.tools.disconnect_wifi_tool,
        #     self.tools.list_bluetooth_tool
        # ]
        self.prompt_embeddings = self.embeddings.embed_documents(self.prompt_templates)

    def route_prompt(self, input_dict):
        query_embedding = self.embeddings.embed_query(input_dict["query"])
        similarity = cosine_similarity([query_embedding], self.prompt_embeddings)[0]
        most_similar_idx = similarity.argmax()

        if most_similar_idx == 0:
            print("Using System")
            return "system"
        else:
            print("Using Chatbot")
            return "chatbot"

    def execute(self, input_query):
        route = self.route_prompt({"query": input_query})
        return {"route": route, "query": input_query}

    def execute_system(self, input_query):

        self.tools = SystemTools()
        self.tools_list = self.tools.return_tools()

        # Create and execute agent
        prompt = hub.pull("hwchase17/structured-chat-agent")
        agent = create_structured_chat_agent(
            llm=self.llm,
            tools=self.tools_list,
            prompt=prompt
        )

        agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools_list,
            verbose=True,
            handle_parsing_errors=True
        )

        result = agent_executor.invoke({
            "input": input_query
        })

        # Process the response if it contains 'output'
        if isinstance(result, dict) and 'output' in result:
            raw_output = result['output']
            analysis_prompt = f"""Based on the output from the system chain:
            {raw_output}

            Please provide a clear analysis of the networks, including:

            The networks with the strongest signals
            What the signal strengths indicate about connection quality
            Recommendations for the best network to connect to
            Present the information in a user-friendly and helpful manner."""

            # Use the LLM to generate a more natural response
            analysis_response = self.llm.invoke(analysis_prompt).content
            return {"raw_output": raw_output, "analysis": analysis_response}

        return result

    def execute_chatbot(self, input_query):
        # Execute chatbot chain
        chain = (
            {"query": RunnablePassthrough()}
            | RunnableLambda(self.route_prompt)
            | self.llm
            | StrOutputParser()
        )
        return chain.invoke(input_query)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    prompt = data.get('prompt', '')

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    router = RouterChain(prompt)
    routing_result = router.execute(prompt)

    if routing_result["route"] == "system":
        return redirect(url_for('chat_system'), code=307)  # 307 preserves the POST method
    else:
        return redirect(url_for('chat_chatbot'), code=307)

@app.route('/chat/system', methods=['POST'])
def chat_system():
    data = request.get_json()
    prompt = data.get('prompt', '')

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    router = RouterChain(prompt)
    response = router.execute_system(prompt)
    return jsonify(response)

@app.route('/chat/chatbot', methods=['POST'])
def chat_chatbot():
    data = request.get_json()
    prompt = data.get('prompt', '')

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    router = RouterChain(prompt)
    response = router.execute_chatbot(prompt)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
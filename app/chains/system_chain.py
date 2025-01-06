from langchain_core.output_parsers import StrOutputParser
from pywifi import const
import time
from langchain.agents import Tool
from app.services.wifi_service import WifiService

class SystemChain:

    def __init__(self, MODEL_PATH, user_prompt):
        self.MODEL_PATH = MODEL_PATH
        self.user_prompt = user_prompt

    def get_template(self):
        template = """You are an expert system assistant. Your primary function is to determine the appropriate chain to use based on the user's request.

                If the user's request is related to controlling system settings or hardware, such as:
                - Changing screen brightness
                - Adjusting volume
                - Managing Wi-Fi connections (turning on/off, connecting to networks)
                - Controlling Bluetooth (pairing devices, turning on/off)
                - Managing system updates
                - Checking system status (battery, memory, etc.)
                - Power management (sleep, restart, shutdown)
                - File system operations (if applicable in your context)

                Then respond with a variation of the text: "Sure, processing the system command!"
                User input: {query}
            """
        return template

class SystemTools(SystemChain):

    def __init__(self, MODEL_PATH, user_prompt):
        super().__init__(MODEL_PATH, user_prompt)

    def tools(self):
        list_wifi_tool = Tool(
            name="list_wifi_networks",
            func=WifiService.list_wifi_networks,
            description="Useful when the user wants to see a list of available Wi-Fi networks.",
        )

        connect_wifi_tool = Tool(
            name="connect_wifi",
            func=WifiService.connect_wifi,
            description="Useful when the user wants to connect to a specific Wi-Fi network.",
        )

        disconnect_wifi_tool = Tool(
            name="disconnect_wifi",
            func=WifiService.disconnect_wifi,
            description="Useful when the user wants to disconnect from the current Wi-Fi network.",
        )

        tools = [list_wifi_tool, connect_wifi_tool, disconnect_wifi_tool]
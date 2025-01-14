from langchain.tools import StructuredTool
from app.services.wifi_service import WifiService

class SystemChain:

    def __init__(self,  user_prompt):
        self.user_prompt = user_prompt

    def get_template(self):
        template = """You are a helpful system assistant that specializes in managing system settings and network connections. When providing information about WiFi networks, you should analyze the available networks and present them in a clear, informative way. Include relevant details about signal strength and explain what the information means for the user.

        If you receive a list of WiFi networks, you should:
        1. Present the networks in a clear format
        2. Highlight the strongest connections
        3. Explain what the signal strength means for connectivity
        4. Provide any relevant recommendations based on the network information

        When working with system commands:
        - For WiFi operations: Present network information in a user-friendly way
        - For other system operations: Clearly explain what actions are being taken
        - Always confirm when operations are completed successfully

        User input: {query}

        Remember to list each fetched network in bullet points and provide a recommendation on which network would be the best to connect to, and a brief explanation in about 50-100 words why you arrived at the same.
        """
        return template

class SystemTools(SystemChain):

    def __init__(self, user_prompt):
        super().__init__(user_prompt)


    list_wifi_tool = StructuredTool.from_function(
            name="list_wifi_networks",
            func=WifiService().list_wifi_networks,
            description="Useful when the user wants to see a list of available Wi-Fi networks.",
        )

    connect_wifi_tool = StructuredTool.from_function(
            name="connect_wifi",
            func=WifiService().connect_wifi,
            description="Useful when the user wants to connect to a specific Wi-Fi network.",
        )

    disconnect_wifi_tool = StructuredTool.from_function(
            name="disconnect_wifi",
            func=WifiService().disconnect_wifi,
            description="Useful when the user wants to disconnect from the current Wi-Fi network.",
        )

from langchain.tools import StructuredTool
from app.services.wifi_service import WifiService
from app.services.bluetooth_service import BluetoothService

class SystemChain:

    def __init__(self,  user_prompt):
        self.user_prompt = user_prompt

    def get_template(self):
        template = """You are a system assistant specializing in managing WiFi and Bluetooth connections. When analyzing networks or devices, present information clearly with relevant details such as signal strength, pairing status, and security.

        WiFi:
        List networks with signal strength and security type.
        Highlight the strongest connections.
        Recommend the best network with a brief explanation.

        Bluetooth:
        List devices with pairing status and signal strength.
        Highlight paired or high-signal devices.
        Recommend the best device to connect with and explain why.

        User Input: {query}

        Confirm actions and summarize results clearly. Keep recommendations concise (50-100 words).
        """
        return template

class SystemTools:
    def __init__(self):
        self.wifi_service = WifiService()

    turn_on_wifi_tool = StructuredTool.from_function(
        name="turn_on_wifi",
        func=lambda: WifiService().turn_on_wifi(),
        description="Turns on WiFi if it's currently disabled."
    )

    list_wifi_tool = StructuredTool.from_function(
        name="list_wifi_networks",
        func=lambda: WifiService().list_wifi_networks(),
        description="Lists available WiFi networks."
    )

    connect_wifi_tool = StructuredTool.from_function(
        name="connect_wifi",
        func=lambda ssid, password: WifiService().connect_wifi(ssid, password),
        description="Connects to a specific WiFi network."
    )

    disconnect_wifi_tool = StructuredTool.from_function(
        name="disconnect_wifi",
        func=lambda: WifiService().disconnect_wifi(),
        description="Disconnects from the current WiFi network."
    )
    list_bluetooth_tool = StructuredTool.from_function(
        name="list_bluetooth_devices",
        func=lambda: BluetoothService().list_bluetooth_devices(),
        description="Lists available Bluetooth devices."
    )

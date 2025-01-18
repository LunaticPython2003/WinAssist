import ctypes

class BluetoothService:
    def __init__(self):
        self.library = ctypes.CDLL("app/services/libraries/DLL/bluetooth.dll")
        self.library.ListBluetoothDevices.restype = ctypes.c_char_p

    def list_bluetooth_devices(self):
        try:
            res = self.library.ListBluetoothDevices()
            return res.decode("utf-8")
        except Exception as e:
            return f"Error listing Bluetooth devices: {str(e)}"


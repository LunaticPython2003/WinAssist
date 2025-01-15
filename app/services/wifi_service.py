import pywifi
from pywifi import const
import os
import time
import subprocess


class WifiService:
    def __init__(self):
        self.wifi = pywifi.PyWiFi()
        self.iface = self.wifi.interfaces()[0]

    def is_wifi_enabled(self):
        try:
            return self.iface.status() != const.IFACE_DISCONNECTED
        except Exception:
            return False

    def turn_on_wifi(self):
        try:

            command = "netsh interface set interface Wi-Fi enable"
            result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
            time.sleep(2)
            return "WiFi has been enabled successfully."
        except subprocess.CalledProcessError as e:
            return f"Failed to enable WiFi: {e.output}"

    def list_wifi_networks(self):
        try:
            if not self.is_wifi_enabled():
                return "WiFi is not turned on."

            self.iface.scan()
            time.sleep(2)
            scan_results = self.iface.scan_results()

            networks = []
            for network in scan_results:
                networks.append({
                    "ssid": network.ssid,
                    "signal": network.signal,
                    "auth": network.akm[0] if network.akm else None
                })

            return f"Available WiFi networks:\n" + "\n".join([
                f"SSID: {net['ssid']}, Signal: {net['signal']}dBm, "
                f"Security: {'Protected' if net['auth'] else 'Open'}"
                for net in networks
            ])
        except Exception as e:
            return f"Error listing WiFi networks: {str(e)}"

    def connect_wifi(self, ssid, password):
        try:
            if not self.is_wifi_enabled():
                return "WiFi is not turned on."

            profile = pywifi.Profile()
            profile.ssid = ssid
            profile.auth = const.AUTH_ALG_OPEN
            profile.akm.append(const.AKM_TYPE_WPA2PSK)
            profile.cipher = const.CIPHER_TYPE_CCMP
            profile.key = password
            self.iface.remove_all_network_profiles()
            tmp_profile = self.iface.add_network_profile(profile)
            self.iface.connect(tmp_profile)
            time.sleep(5)
            return "Successfully connected to WiFi." if self.iface.status() == const.IFACE_CONNECTED else "Failed to connect to WiFi."
        except Exception as e:
            return f"Error connecting to WiFi: {str(e)}"

    def disconnect_wifi(self):
        try:
            if not self.is_wifi_enabled():
                return "WiFi is not turned on."

            self.iface.disconnect()
            time.sleep(2)
            return "Successfully disconnected from WiFi." if self.iface.status() == const.IFACE_DISCONNECTED else "Failed to disconnect from WiFi."
        except Exception as e:
            return f"Error disconnecting from WiFi: {str(e)}"

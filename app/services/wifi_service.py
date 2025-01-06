import pywifi
from pywifi import const
import time

class WifiService:
    def __init__(self):
        self.wifi = pywifi.PyWiFi()
        self.iface = self.wifi.interfaces()[0]

    def list_wifi_networks(self):

        try:
            self.iface.scan()  # Trigger a scan for networks
            time.sleep(2)  # Wait for the scan to complete
            scan_results = self.iface.scan_results()  # Get the scan results

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
        return self.iface.status() == const.IFACE_CONNECTED

    def disconnect_wifi(self):
        self.iface.disconnect()
        time.sleep(2)
        return self.iface.status() == const.IFACE_DISCONNECTED
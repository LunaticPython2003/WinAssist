#include <Windows.h>
#include <bluetoothapis.h>
#include <string>
#pragma comment(lib, "Bthprops.lib")

// Function to list Bluetooth Devices
extern "C" __declspec(dllexport) const char* ListBluetoothDevices() {
    static std::string output;
    output.clear();
    BLUETOOTH_DEVICE_SEARCH_PARAMS searchParams;
    ZeroMemory(&searchParams, sizeof(searchParams));
    searchParams.dwSize               = sizeof(BLUETOOTH_DEVICE_SEARCH_PARAMS);
    searchParams.fReturnAuthenticated = TRUE;
    searchParams.fReturnRemembered    = TRUE;
    searchParams.fReturnUnknown       = TRUE;
    searchParams.fReturnConnected     = TRUE;
    searchParams.hRadio               = NULL;

    BLUETOOTH_DEVICE_INFO deviceInfo;
    ZeroMemory(&deviceInfo, sizeof(deviceInfo));
    deviceInfo.dwSize = sizeof(BLUETOOTH_DEVICE_INFO);

    HBLUETOOTH_DEVICE_FIND hFind = BluetoothFindFirstDevice(&searchParams, &deviceInfo);
    if (hFind) {
        do {
            output += "Device Name: ";
            std::wstring wName(deviceInfo.szName);
            output.append(wName.begin(), wName.end());
            output += "\nAddress: ";
            for (int i = 5; i >= 0; --i) {
                char buf[4];
                sprintf_s(buf, "%02X", deviceInfo.Address.rgBytes[i]);
                output += buf;
                if (i > 0) output += ":";
            }
            output += "\nConnected: ";
            output += (deviceInfo.fConnected ? "Yes" : "No");
            output += "\nRemembered: ";
            output += (deviceInfo.fRemembered ? "Yes" : "No");
            output += "\nAuthenticated: ";
            output += (deviceInfo.fAuthenticated ? "Yes" : "No");
            output += "\n\n";
        } while (BluetoothFindNextDevice(hFind, &deviceInfo));
        BluetoothFindDeviceClose(hFind);
    } else {
        output = "No Bluetooth devices found or error occurred.\n";
    }
    return output.c_str();
}

extern "C" __declspec(dllexport) bool ConnectBluetoothDevice(const char* macAddress) {
    std::string target(macAddress);
    BLUETOOTH_DEVICE_SEARCH_PARAMS searchParams;
    ZeroMemory(&searchParams, sizeof(searchParams));
    searchParams.dwSize               = sizeof(BLUETOOTH_DEVICE_SEARCH_PARAMS);
    searchParams.fReturnAuthenticated = TRUE;
    searchParams.fReturnRemembered    = TRUE;
    searchParams.fReturnUnknown       = TRUE;
    searchParams.fReturnConnected     = TRUE;
    searchParams.hRadio               = NULL;

    BLUETOOTH_DEVICE_INFO deviceInfo;
    ZeroMemory(&deviceInfo, sizeof(deviceInfo));
    deviceInfo.dwSize = sizeof(BLUETOOTH_DEVICE_INFO);

    HBLUETOOTH_DEVICE_FIND hFind = BluetoothFindFirstDevice(&searchParams, &deviceInfo);
    if (hFind) {
        do {
            char addressBuf[18];
            sprintf_s(addressBuf, "%02X:%02X:%02X:%02X:%02X:%02X",
                deviceInfo.Address.rgBytes[5],
                deviceInfo.Address.rgBytes[4],
                deviceInfo.Address.rgBytes[3],
                deviceInfo.Address.rgBytes[2],
                deviceInfo.Address.rgBytes[1],
                deviceInfo.Address.rgBytes[0]);
            if (_stricmp(addressBuf, target.c_str()) == 0) {
                BluetoothFindDeviceClose(hFind);
                return true;
            }
        } while (BluetoothFindNextDevice(hFind, &deviceInfo));
        BluetoothFindDeviceClose(hFind);
    }
    return false;
}
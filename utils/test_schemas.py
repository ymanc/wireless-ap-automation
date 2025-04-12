# test_schemas.py
# Author(s): Wai Man Cheng, ChatGPT (OpenAI 4.0 AI Assistant)
# Description:
# ------------
# This file defines reusable test parameter schemas for different test types.
# Each test type (performance, security, roaming, etc.) has its own schema
#to define what parameters are needed and their default values.

TEST_SCHEMAS = {
    "performance": {
        "wifi_standard": "11ax",
        "client_type": "windows_intel",
        "traffic_type": "UDP",
        "direction": "DL",
        "duration": 300,
        "ssid": "ssid_wpa3_sae",
        "security_type": "wpa3-sae",
        "radio_band": "6G",
        "bandwidth": "80MHz",
        "nss": 2
    },
    "security": {
        "ssid": "ssid_wpa3_sae",
        "auth_method": "SAE",
        "encryption": "AES",
        "client_type": "windows_intel",
        "radio_band": "6G"
    },
    "roaming": {
        "ssid": "roaming_ssid",
        "client_type": "android_qca",
        "roaming_type": "11r",
        "initial_ap": "ap1",
        "target_ap": "ap2",
        "radio_band": "5G"
    }
}

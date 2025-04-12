"""
File: connect_devices.py
Author(s): Wai Man Cheng, ChatGPT (OpenAI 4.0 AI Assistant)
Date: 2025-04-09

Description:
------------
This module connects to specified testbed devices using pyATS.
It supports SSH login to AP and sniffer nodes, and verifies whether 
any wireless clients are connected to the AP by executing and parsing 
'show dot11 clients' output (Cisco baseline).

Purpose:
--------
- Connect to devices from testbed.yaml using pyATS
- Validate AP connectivity
- Confirm that at least one wireless client is associated

Inputs:
-------
- A pyATS `testbed.yaml` file
- A list of device names to connect

Outputs:
--------
- Dictionary of connected device objects
- Prints connection and validation status
- (Later enhancement: Save session state to JSON/YAML)

Dependencies:
-------------
- pyATS
- parsers.client_parser (used to extract client info from CLI)

License:
--------
MIT License with attribution encouraged.
This is part of an open-source AI-assisted QA Automation Framework 
for wireless and network device testing. Contributions welcome.

Copyright © 2025 Wai Man Cheng
"""

from pyats.topology import loader
from unicon.core.errors import ConnectionError

class DeviceConnector:
    def __init__(self, testbed_path: str):
        """
        Load the testbed YAML file and initialize the testbed.
        """
        self.testbed = loader.load(testbed_path)
        self.devices = {}

    def connect(self, device_names):
        """
        Attempt SSH connection to each device in device_names.
        """
        for name in device_names:
            if name in self.testbed.devices:
                dev = self.testbed.devices[name]
                try:
                    dev.connect()
                    self.devices[name] = dev
                    print(f"[CONNECTED] {name}")
                except ConnectionError as e:
                    print(f"[FAILED] {name}: {e}")
            else:
                print(f"[MISSING] {name} not found in testbed")

        return self.devices

    def verify_client_connected(self, ap_name="ap"):
        """
        Run show dot11 clients on AP, parse to check if any client is connected.
        """
        if ap_name not in self.devices:
            raise ValueError("AP not connected.")

        ap = self.devices[ap_name]
        output = ap.execute("show dot11 clients")
        from parsers.client_parser import extract_clients
        clients = extract_clients(output)

        if clients:
            print(f"✅ {len(clients)} client(s) connected.")
            return True
        else:
            print("❌ No wireless client connected.")
            return False

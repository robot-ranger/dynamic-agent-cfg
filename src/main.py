from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
import logging
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

mtc_schema_ver = "2.2"
streams_ns = {"":f'urn:mtconnect.org:MTConnectStreams:{mtc_schema_ver}'}
devices_ns = {"":f'urn:mtconnect.org:MTConnectDevices:{mtc_schema_ver}'}

# setup logging
log = logging.getLogger("uvicorn.error")
log.setLevel(logging.DEBUG)

app = FastAPI()

agent_host = "192.168.0.105"
agent_port = 5000

@app.get("/devices")
def parse_mtconnect():
    # Make a GET request to the URL
    response = requests.get(f"http://{agent_host}:{agent_port}/probe", timeout=0.5)
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        
        # Extract the data from the XML and create collapsible list groups
        devices = []
        print(root.find(".//Devices", devices_ns))
        for device in root.find(".//Devices", devices_ns):
            device_data = {}
            device_data.update({k: v for k, v in device.attrib.items()})
            print(device_data)
            device_data.update({"components": []})
            for component in device.find(".//Components", devices_ns):
                component_data = {}
                component_data.update({k: v for k, v in component.attrib.items()})
                device_data["components"].append(component_data)
            
            devices.append(device_data)
        print(devices)
        
        return devices
    else:
        return {"error": "could not connect to agent"}

@app.get("/config")
def configure():
    return {"configure": "configure"}

@app.post("/config")
def configure():
    return {"configure": "configure"}

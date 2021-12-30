
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import paho.mqtt.client as mqtt
import uvicorn
from PIL import Image
import base64
from io import BytesIO


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

def on_connect(client, userdata, flags, rc):  # The callback for when the client connects to the broker
    print("Connected with result code {0}".format(str(rc)))  # Print result of connection attempt
    client.subscribe("pic/img")  # Subscribe to the topic “digitest/test1”, receive any messages published on it


def on_message(client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
    print("Message received-> " + msg.topic + " " + str(msg.payload))  # Print a received msg
    codd = msg.payload
    
    with open('decoded_image.png', 'wb') as file_to_save:
        decoded_image_data = base64.decodebytes(codd)
        file_to_save.write(decoded_image_data)

@app.get("/detection")
async def getDetection():
    client = mqtt.Client("digi_mqtt_test")  # Create instance of client with client ID “digi_mqtt_test”
    client.on_connect = on_connect  # Define callback function for successful connection
    client.on_message = on_message  # Define callback function for receipt of a message
    # client.connect("m2m.eclipse.org", 1883, 60)  # Connect to (broker, port, keepalive-time)
    client.connect('broker.emqx.io', 1883)
    client.loop_forever()  # Start networking daemon
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
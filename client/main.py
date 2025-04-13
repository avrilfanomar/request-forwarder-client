import os
import shlex
import subprocess
import paho.mqtt.client as mqtt_client
import paho.mqtt as mqtt
import urllib.parse

# Configuration
MQTT_BROKER = os.getenv("REQUEST_FORWARDER_BROKER", "37.157.254.65")
TOPIC = "req/" + os.getenv("REQUEST_FORWARDER_TOKEN", "NO_TOKEN_SET")
MODE = os.getenv("REQUEST_FORWARDER_MODE", "exec")
if TOPIC == "req/NO_TOKEN_SET":
    print("No token present. Please set the REQUEST_FORWARDER_TOKEN environment variable.")
    exit(1)


def execute_command(command):
    try:
        print(f"Executing...")
        args = shlex.split(command)  # Safe parsing of shell command
        for arg in args:
            if arg.startswith("http://") or arg.startswith("https://"):
                parsed = urllib.parse.urlparse(arg)
                host = parsed.hostname
                if host not in ["localhost", "127.0.0.1", "::1"]:
                    print(f"Invalid URL host: {host}")
                    return
        result = subprocess.run(args, capture_output=True, text=True, check=True)
        print("Output:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error:", e.stderr)


def on_message(client, userdata, msg):
    command = msg.payload.decode().strip()
    print(f"Received: {command}")
    if MODE == "exec":
        execute_command(command)


def subscribe():
    client = mqtt_client.Client(client_id="",
                                protocol=mqtt_client.MQTTv5,
                                callback_api_version=mqtt.enums.CallbackAPIVersion.VERSION2)
    client.on_message = on_message
    client.connect(MQTT_BROKER)
    client.subscribe(TOPIC)
    print(f"Subscribed to {TOPIC} on {MQTT_BROKER}. Waiting for commands...")
    client.loop_forever()


if __name__ == "__main__":
    subscribe()

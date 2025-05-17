import os
import shlex
import subprocess
import paho.mqtt.client as mqtt_client
import paho.mqtt as mqtt
import urllib.parse
import sys

# Default configuration values
DEFAULT_MQTT_BROKER = "37.157.254.65"
DEFAULT_TOKEN = "NO_TOKEN_SET"
DEFAULT_MODE = "exec"
DEFAULT_CERTIFICATE_CHECK_IGNORE = "false"

def get_config():
    """Get configuration from environment variables."""
    mqtt_broker = os.getenv("REQUEST_FORWARDER_BROKER", DEFAULT_MQTT_BROKER)
    token = os.getenv("REQUEST_FORWARDER_TOKEN", DEFAULT_TOKEN)
    topic = "req/" + token
    mode = os.getenv("REQUEST_FORWARDER_MODE", DEFAULT_MODE)
    scheme = os.getenv("REQUEST_FORWARDER_OVERRIDE_SCHEME")
    redirect_url = os.getenv("REQUEST_FORWARDER_REDIRECT_URL")
    override_port = os.getenv("REQUEST_FORWARDER_OVERRIDE_PORT")
    override_path = os.getenv("REQUEST_FORWARDER_OVERRIDE_PATH")
    certificate_check_ignore = os.getenv("REQUEST_FORWARDER_CERTIFICATE_CHECK_IGNORE", DEFAULT_CERTIFICATE_CHECK_IGNORE)

    return {
        "mqtt_broker": mqtt_broker,
        "token": token,
        "topic": topic,
        "mode": mode,
        "scheme": scheme,
        "redirect_url": redirect_url,
        "override_port": override_port,
        "override_path": override_path,
        "certificate_check_ignore": certificate_check_ignore
    }

# Get configuration
config = get_config()

def validate_environment_variables(config=None):
    """
    Validate environment variables and return a list of errors if any.

    Args:
        config (dict, optional): Configuration dictionary. If None, uses global config.

    Returns:
        list: List of error messages, empty if no errors
    """
    if config is None:
        config = get_config()

    errors = []

    # Check required variables
    if config["topic"] == "req/NO_TOKEN_SET":
        errors.append("No token present. Please set the REQUEST_FORWARDER_TOKEN environment variable.")

    # Validate MODE - only 'exec' is supported
    if config["mode"] != "exec":
        errors.append(f"Invalid MODE: {config['mode']}. Supported modes: exec")

    # Validate CERTIFICATE_CHECK_IGNORE
    if config["certificate_check_ignore"].lower() not in ["true", "false"]:
        errors.append(f"Invalid CERTIFICATE_CHECK_IGNORE: {config['certificate_check_ignore']}. Must be 'true' or 'false'.")

    # Validate OVERRIDE_PORT if set
    if config["override_port"] and not config["override_port"].isdigit():
        errors.append(f"Invalid OVERRIDE_PORT: {config['override_port']}. Must be a number.")

    # Validate REDIRECT_URL if set
    if config["redirect_url"]:
        try:
            urllib.parse.urlparse(config["redirect_url"])
        except Exception as e:
            errors.append(f"Invalid REDIRECT_URL: {config['redirect_url']}. Error: {str(e)}")

    return errors

# Validate environment variables
errors = validate_environment_variables(config)
if errors:
    for error in errors:
        print(error)
    sys.exit(1)

def modify_url(url, config=None):
    """
    Modify the URL based on configuration.

    Args:
        url (str): The URL to modify
        config (dict, optional): Configuration dictionary. If None, uses global config.

    Returns:
        str: The modified URL
    """
    if config is None:
        config = get_config()

    parsed = urllib.parse.urlparse(url)
    scheme = config["scheme"] if config["scheme"] else parsed.scheme
    netloc = parsed.netloc
    path = parsed.path
    query = parsed.query
    fragment = parsed.fragment

    # Apply redirect URL if specified
    if config["redirect_url"]:
        forward_parsed = urllib.parse.urlparse(config["redirect_url"])
        # Use the redirect URL's scheme if it has one, otherwise keep the original or override
        if forward_parsed.scheme:
            scheme = forward_parsed.scheme
        # Use the redirect URL's netloc if it has one, otherwise keep the original
        if forward_parsed.netloc:
            netloc = forward_parsed.netloc

    # Apply scheme override if specified (this takes precedence over redirect URL)
    if config["scheme"]:
        scheme = config["scheme"]

    # Apply path override if specified
    if config["override_path"]:
        path = config["override_path"]

    # Apply port override if specified
    if config["override_port"]:
        # Split netloc into host and port
        host_parts = netloc.split(':')
        host = host_parts[0]
        # Reconstruct netloc with overridden port
        netloc = f"{host}:{config['override_port']}"

    return urllib.parse.urlunparse((scheme, netloc, path, '', query, fragment))

def execute_command(command, config=None):
    """
    Execute a command with URL modifications.

    Args:
        command (str): The command to execute
        config (dict, optional): Configuration dictionary. If None, uses global config.
    """
    if config is None:
        config = get_config()

    try:
        args = shlex.split(command)  # Safe parsing of shell command
        new_args = []
        for arg in args:
            if arg.startswith("http://") or arg.startswith("https://"):
                parsed = urllib.parse.urlparse(arg)
                host = parsed.hostname
                if host not in ["localhost", "127.0.0.1", "::1"]:
                    print(f"Invalid URL host: {host}")
                    return
                # Apply modifications
                arg = modify_url(arg, config)
            new_args.append(arg)
        if config["certificate_check_ignore"].lower() == "true":
            new_args.append("-k")
        print("Modified args:", new_args)
        print(f"Executing...")
        result = subprocess.run(new_args, capture_output=True, text=True, check=True)
        print("Output:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error:", e.stderr)


def on_message(client, userdata, msg, config=None):
    """
    Handle incoming MQTT messages.

    Args:
        client: MQTT client instance
        userdata: User data
        msg: MQTT message
        config (dict, optional): Configuration dictionary. If None, uses global config.
    """
    if config is None:
        config = get_config()

    command = msg.payload.decode().strip()
    print(f"Received: {command}")
    if config["mode"] == "exec":
        execute_command(command, config)


def subscribe(config=None):
    """
    Subscribe to MQTT topic and listen for commands.

    Args:
        config (dict, optional): Configuration dictionary. If None, uses global config.
    """
    if config is None:
        config = get_config()

    client = mqtt_client.Client(client_id="",
                                protocol=mqtt_client.MQTTv5,
                                callback_api_version=mqtt.enums.CallbackAPIVersion.VERSION2)
    client.on_message = lambda client, userdata, msg: on_message(client, userdata, msg, config)
    client.connect(config["mqtt_broker"])
    client.subscribe(config["topic"])
    print(f"Subscribed to {config['topic']} on {config['mqtt_broker']}. Waiting for commands...")
    client.loop_forever()


if __name__ == "__main__":
    subscribe()

# Request Forwarder Client

A lightweight client for receiving and executing requests from request forwarder server.

## Installation
```sh
pipx install request-forwarder-client
```

Mandatory OS variable:
```sh
export REQUEST_FORWARDER_TOKEN=<your_token>
```

Optional OS variables:
```sh
# MQTT broker address (default: 37.157.254.65)
export REQUEST_FORWARDER_BROKER=<your custom server ip/host>

# Mode of operation (default: 'exec')
# 'exec': Execute the received command
# Any other value: Just print the received command without executing it
export REQUEST_FORWARDER_MODE=<anything except 'exec' will just print the request>

# Override the scheme (http/https) of URLs in commands
export REQUEST_FORWARDER_OVERRIDE_SCHEME=<http/https>

# Redirect requests to a different URL
# Example: https://newhost:9090
export REQUEST_FORWARDER_REDIRECT_URL=<url>

# Override the port in URLs
export REQUEST_FORWARDER_OVERRIDE_PORT=<port>

# Override the path in URLs
export REQUEST_FORWARDER_OVERRIDE_PATH=<path>

# Ignore certificate checks (add -k flag to curl commands)
# Values: true, false (default: false)
export REQUEST_FORWARDER_CERTIFICATE_CHECK_IGNORE=<true|false>
```

## Run
```sh
request-forwarder-client
```

## License
This project is licensed under the Apache 2.0 license. See the [LICENSE](LICENSE) file for details.

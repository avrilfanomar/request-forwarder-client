# Request Forwarder Client

A lightweight client for receiving and executing requests from request forwarder server.

Mandatory OS variable:
```sh
export REQUEST_FORWARDER_TOKEN=<your_token>
```

Optional OS variables:
```sh
export REQUEST_FORWARDER_BROKER=<your custom server ip/host>
export REQUEST_FORWARDER_MODE=<anything except 'exec' will just print the request>
```

## Installation
```sh
pip install request-forwarder-client
```

## License
This project is licensed under the Apache 2.0 license. See the [LICENSE](LICENSE) file for details.

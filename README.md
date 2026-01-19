 L4D2 RCON Controller

# L4D2 RCON Controller (Python)

![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue) ![Left 4 Dead 2](https://img.shields.io/badge/Game-Left%204%20Dead%202-green) ![RCON](https://img.shields.io/badge/Protocol-RCON-orange) ![MIT License](https://img.shields.io/badge/License-MIT-lightgrey) ![Windows | Linux](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-blueviolet)

A lightweight, interactive **RCON client for Left 4 Dead 2** written in Python. This tool allows server administrators to connect to a Source engine server and execute RCON commands with real-time feedback.

- - -

## Features

*   Source RCON protocol implementation
*   Designed for Left 4 Dead 2
*   Interactive command-line interface
*   Terminal loading animations
*   Threaded networking
*   No external dependencies

- - -

## Requirements

*   Python 3.8 or newer
*   Left 4 Dead 2 dedicated server
*   RCON enabled on the server

- - -

## Configuration

Edit the following values at the top of the script:

HOST = "123.123.123.123" \
PORT = 27015 \
PASSWORD = "YOUR\_RCON\_PASSWORD"

Make sure RCON is enabled on your server:

rcon\_password "your\_password"

- - -

## Usage

Run the script:

python l4d2\_rcon.py

Example commands:

RCON> status\
RCON> sm plugins list\
RCON> changelevel c2m1\_highway

Exit the client with:

exit \
quit \
Ctrl + C

- - -

## How It Works

*   Uses the Source RCON binary protocol
*   Authenticates using SERVERDATA\_AUTH
*   Executes commands using SERVERDATA\_EXECCOMMAND
*   Handles multi-packet responses
*   Displays progress using terminal animations

- - -

## Project Structure

. \
├── l4d2\_rcon.py \
└── README.html

- - -

## Security Notes

*   Do not commit your real RCON password
*   Use environment variables if deploying publicly
*   RCON provides full server control

- - -

## License

MIT License

- - -

## Author

Pablo Santillan

- - -

## Contributing

Pull requests and improvements are welcome.\Open an issue for bugs, ideas, or enhancements.

- - -

## Tested With

*   Left 4 Dead 2 (Source Engine)
*   Linux and Windows dedicated servers
*   Python 3.8 – 3.12

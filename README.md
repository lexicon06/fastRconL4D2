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


### Interactive Mode

Run the script for an interactive RCON session:

```bash
python l4d2_rcon.py
```

You'll get an interactive prompt where you can enter commands:

```
==================================================
L4D2 RCON Controller
==================================================
Connecting to 127.0.0.1:27015...
Authentication successful
Connected! Type 'exit' or press Ctrl+C to quit.
==================================================

RCON> status
--------------------------------------------------
hostname: My L4D2 Server
version : 2.2.3.2
udp/ip  : 192.168.1.100:27015
map     : c1m1_hotel at: 0 x, 0 y, 0 z
players : 4 humans, 0 bots (8 max)
--------------------------------------------------

RCON> say Hello players!
--------------------------------------------------
--------------------------------------------------

RCON> exit
Disconnecting...
Disconnected. Goodbye!
```

### Programmatic Usage

You can also use the RCON class in your own Python scripts:

```python
from l4d2_rcon import L4D2RCON

# Create instance
rcon = L4D2RCON("127.0.0.1", 27015, "your_password")

# Connect
if rcon.connect():
    # Execute commands
    response = rcon.execute("status")
    print(response)
    
    # Change map
    rcon.execute("changelevel c2m1_highway")
    
    # Send message
    rcon.execute('say "Server maintenance in 5 minutes!"')
    
    # Disconnect
    rcon.disconnect()
```

## Common L4D2 RCON Commands

| Command | Description |
|---------|-------------|
| `status` | Display server status and player list |
| `maps *` | List all available maps |
| `changelevel <map>` | Change to specified map |
| `say "<message>"` | Send message to all players |
| `kick <player>` | Kick a player by name |
| `sm_cvar <var> <value>` | Change server variable (requires SourceMod) |
| `sm_ban <player> <time>` | Ban a player (requires SourceMod) |
| `sm_kick <player>` | Kick player (requires SourceMod) |
| `quit` | Shutdown the server |



## License

MIT License

- - -

## Author

Pablo Santillan

- - -

## Contributing

Pull requests and improvements are welcome. Open an issue for bugs, ideas, or enhancements.

- - -

## Tested With

*   Left 4 Dead 2 (Source Engine)
*   Linux and Windows dedicated servers
*   Python 3.8 – 3.12

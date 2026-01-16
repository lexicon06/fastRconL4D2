# L4D2 RCON Controller

A simple and efficient Python-based RCON (Remote Console) client for Left 4 Dead 2 servers. Control your game server with ease through a command-line interface.

## Features

- ✅ Full Source RCON protocol implementation
- ✅ Interactive command-line interface
- ✅ Multi-packet response handling
- ✅ Secure password authentication
- ✅ Clean error handling and timeout management
- ✅ Simple and lightweight (single file)

## Requirements

- Python 3.6 or higher
- Network access to your L4D2 server's RCON port

## Installation

1. Clone this repository:
```bash
git clone https://github.com/lexicon06/l4d2-rcon-controller.git
cd l4d2-rcon-controller
```

2. No external dependencies required! Uses only Python standard library.

## Configuration

Edit the script and update the connection details:

```python
HOST = "127.0.0.1"              # Your server IP
PORT = 27015                     # RCON port (default: 27015)
PASSWORD = "your_rcon_password"  # Your RCON password
```

### Setting up RCON on your L4D2 Server

Add these lines to your `server.cfg`:

```
rcon_password "your_secure_password"
hostport 27015
```

Make sure your firewall allows connections to the RCON port.

## Usage

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

## Exiting the Program

- Type `exit`, `quit`, or `q` in the interactive prompt
- Press `Ctrl+C` at any time

## Troubleshooting

### Connection Failed
- Check that your server IP and port are correct
- Verify RCON password matches your server configuration
- Ensure firewall allows connections to the RCON port
- Confirm the server is running

### Authentication Failed
- Double-check your RCON password in `server.cfg`
- Make sure `rcon_password` is set on the server

### No Response from Server
- Some commands don't return output (e.g., `say`)
- Check server console for command execution
- Verify the command syntax is correct

### Connection Timeout
- Default timeout is 10 seconds
- Increase timeout in `__init__` if needed for slow connections:
  ```python
  self.sock.settimeout(30)  # 30 seconds
  ```

## Protocol Details

This implementation follows the [Valve Source RCON Protocol](https://developer.valvesoftware.com/wiki/Source_RCON_Protocol):

- **SERVERDATA_AUTH (3)**: Authentication request
- **SERVERDATA_AUTH_RESPONSE (2)**: Authentication response  
- **SERVERDATA_EXECCOMMAND (2)**: Command execution
- **SERVERDATA_RESPONSE_VALUE (0)**: Command response

## License

MIT License - feel free to use and modify as needed.

## Contributing

Contributions are welcome! Feel free to:

- Report bugs
- Suggest new features
- Submit pull requests

## Credits

Developed by **Pablo Santillan** ([@lexicon06](https://github.com/lexicon06)) for easy L4D2 server management. Based on the Source RCON protocol specification.

## Disclaimer

Use this tool responsibly. Always ensure you have permission to access and control the server you're connecting to.

---

**Note**: This tool works with any Source engine game that supports RCON (CS:GO, TF2, CS:S, etc.), not just L4D2. Simply adjust the commands accordingly.

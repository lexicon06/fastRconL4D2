import socket
import struct
import time
import threading
import sys

# ============================================================================
# RCON PROTOCOL CONSTANTS
# ============================================================================
# These match the Source RCON protocol definitions
SERVERDATA_AUTH = 3
SERVERDATA_AUTH_RESPONSE = 2
SERVERDATA_EXECCOMMAND = 2
SERVERDATA_RESPONSE_VALUE = 0

# Connection configuration - EDIT THESE VALUES
HOST = "123.123.123.123"           # Server IP address
PORT = 27015                       # RCON port (default: 27015)
PASSWORD = "YOUR_RCON_PASSWORD"    # Your RCON password

# Loading animation constants
SPINNER_CHARS = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
DOTS_CHARS = ['   ', '.  ', '.. ', '...']
SIMPLE_SPINNER_CHARS = '|/-\\'

# Network settings
SOCKET_TIMEOUT = 10
PACKET_SLEEP_TIME = 0.1
ANIMATION_SPEED = 0.1
# ============================================================================

class L4D2RCON:
    """Simple RCON client for Left 4 Dead 2 server"""
    
    def __init__(self, host=None, port=None, password=None):
        """Initialize RCON client with optional overrides"""
        self.host = host or HOST
        self.port = port or PORT
        self.password = password or PASSWORD
        self.sock = None
        self.req_id = 0
        
    def connect(self):
        """Connect to the RCON server"""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(SOCKET_TIMEOUT)
            self.sock.connect((self.host, self.port))
            return self._authenticate()
        except Exception as e:
            print(f"Connection error: {e}")
            return False
    
    def disconnect(self):
        """Close the connection"""
        if self.sock:
            self.sock.close()
            self.sock = None
    
    def _send_packet(self, pkt_type, body):
        """Send an RCON packet"""
        self.req_id += 1
        body_encoded = body.encode('utf-8')
        size = len(body_encoded) + 10  # 4 bytes size + 4 bytes ID + 4 bytes type + 2 null terminators
        
        packet = struct.pack('<iii', size, self.req_id, pkt_type)
        packet += body_encoded
        packet += b'\x00\x00'
        
        self.sock.sendall(packet)
        return self.req_id
    
    def _receive_packet(self):
        """Receive an RCON packet"""
        try:
            # Read packet size (4 bytes)
            size_data = self.sock.recv(4)
            if not size_data or len(size_data) < 4:
                return None, None, None
            
            size = struct.unpack('<i', size_data)[0]
            
            # Read the actual packet data
            body = b''
            while len(body) < size:
                chunk = self.sock.recv(size - len(body))
                if not chunk:
                    break
                body += chunk
            
            if len(body) < size:
                return None, None, None
            
            # Parse packet: ID (4 bytes) + Type (4 bytes) + Body (rest)
            req_id, pkt_type = struct.unpack('<ii', body[:8])
            body_text = body[8:-2].decode('utf-8', errors='ignore')  # Remove 2 null terminators
            
            return req_id, pkt_type, body_text
        except socket.timeout:
            return None, None, None
        except Exception as e:
            print(f"Receive error: {e}")
            return None, None, None
    
    def _authenticate(self):
        """Authenticate with the server"""
        self._send_packet(SERVERDATA_AUTH, self.password)
        time.sleep(PACKET_SLEEP_TIME)
        
        # First packet is a dummy SERVERDATA_RESPONSE_VALUE with ID -1
        req_id, pkt_type, body = self._receive_packet()
        
        # Second packet contains the actual auth response
        req_id, pkt_type, body = self._receive_packet()
        
        if req_id == -1:
            print("Authentication failed: Invalid password")
            return False
        
        print("Authentication successful")
        return True
    
    def execute(self, command):
        """Execute an RCON command and return the response"""
        if not self.sock:
            print("Not connected. Call connect() first.")
            return None
        
        try:
            # Start loading animation
            animation_thread = LoadingAnimation()
            animation_thread.start()
            
            sent_id = self._send_packet(SERVERDATA_EXECCOMMAND, command)
            
            # Collect all response packets
            response = ''
            while True:
                req_id, pkt_type, body = self._receive_packet()
                
                if req_id is None:
                    break
                
                # Stop when we get a response with different ID or empty body
                if req_id == sent_id and pkt_type == SERVERDATA_RESPONSE_VALUE:
                    response += body
                else:
                    break
            
            # Stop animation and return response
            animation_thread.stop()
            animation_thread.join()
            
            return response.strip()
        except Exception as e:
            # Make sure to stop animation if an error occurs
            if 'animation_thread' in locals():
                animation_thread.stop()
                animation_thread.join()
            print(f"Command execution error: {e}")
            return None


class LoadingAnimation:
    """Loading animation that runs in a separate thread"""
    
    def __init__(self, message="Waiting for server response"):
        self.message = message
        self.running = False
        self.thread = None
    
    def start(self):
        """Start the animation thread"""
        self.running = True
        self.thread = threading.Thread(target=self._animate)
        self.thread.daemon = True
        self.thread.start()
    
    def stop(self):
        """Stop the animation"""
        self.running = False
    
    def _animate(self):
        """Animation loop"""
        i = 0
        dot_i = 0
        start_time = time.time()
        
        while self.running:
            # Clear line and show animation
            sys.stdout.write('\r')
            sys.stdout.flush()
            
            # Different animation styles based on elapsed time
            elapsed = time.time() - start_time
            
            if elapsed < 3:
                # Spinner for first 3 seconds
                spinner = SPINNER_CHARS[i % len(SPINNER_CHARS)]
                sys.stdout.write(f"{spinner} {self.message}")
            elif elapsed < 10:
                # Dots animation for next 7 seconds
                dots = DOTS_CHARS[dot_i % len(DOTS_CHARS)]
                sys.stdout.write(f"⏳ {self.message}{dots}")
            else:
                # Show elapsed time after 10 seconds
                elapsed_str = f"{elapsed:.1f}s"
                sys.stdout.write(f"🕒 {self.message} (waiting {elapsed_str})")
            
            sys.stdout.flush()
            
            i += 1
            dot_i += 1
            time.sleep(ANIMATION_SPEED)
        
        # Clear the animation line when done
        sys.stdout.write('\r' + ' ' * 80 + '\r')
        sys.stdout.flush()
    
    def join(self):
        """Wait for animation thread to finish"""
        if self.thread:
            self.thread.join(timeout=1)


class SimpleSpinner:
    """Simpler loading spinner"""
    
    def __init__(self, message="Processing"):
        self.message = message
        self.running = False
        self.thread = None
    
    def start(self):
        """Start the animation thread"""
        self.running = True
        self.thread = threading.Thread(target=self._animate)
        self.thread.daemon = True
        self.thread.start()
    
    def stop(self):
        """Stop the animation"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)
            sys.stdout.write('\r' + ' ' * 50 + '\r')
            sys.stdout.flush()
    
    def _animate(self):
        """Animation loop"""
        i = 0
        while self.running:
            sys.stdout.write(f'\r{SIMPLE_SPINNER_CHARS[i % len(SIMPLE_SPINNER_CHARS)]} {self.message}... ')
            sys.stdout.flush()
            time.sleep(ANIMATION_SPEED)
            i += 1


# Main execution
if __name__ == "__main__":
    print("=" * 50)
    print("L4D2 RCON Controller")
    print("=" * 50)
    print(f"Connecting to {HOST}:{PORT}...")
    
    # Show connecting animation
    print("Connecting", end="", flush=True)
    for i in range(3):
        time.sleep(0.5)
        print(".", end="", flush=True)
    print()
    
    # Create RCON instance
    rcon = L4D2RCON()
    
    # Connect to server
    if not rcon.connect():
        print("Failed to connect to server")
        exit(1)
    
    print("Connected! Type 'exit' or press Ctrl+C to quit.")
    print("=" * 50)
    
    try:
        while True:
            # Get command from user
            try:
                command = input("\nRCON> ").strip()
            except EOFError:
                break
            
            # Check for exit command
            if command.lower() in ['exit', 'quit', 'q']:
                print("Disconnecting...")
                break
            
            # Skip empty commands
            if not command:
                continue
            
            # Execute command
            response = rcon.execute(command)
            
            # Display response
            if response:
                print("-" * 50)
                print(response)
                print("-" * 50)
            else:
                print("No response or error occurred")
    
    except KeyboardInterrupt:
        print("\n\nCtrl+C detected. Disconnecting...")
    
    finally:
        rcon.disconnect()
        print("Disconnected. Goodbye!")

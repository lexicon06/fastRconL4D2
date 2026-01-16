import socket
import struct
import time

class L4D2RCON:
    """Simple RCON client for Left 4 Dead 2 server"""
    
    SERVERDATA_AUTH = 3
    SERVERDATA_AUTH_RESPONSE = 2
    SERVERDATA_EXECCOMMAND = 2
    SERVERDATA_RESPONSE_VALUE = 0
    
    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        self.password = password
        self.sock = None
        self.req_id = 0
        
    def connect(self):
        """Connect to the RCON server"""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(10)
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
        size = len(body_encoded) + 10
        
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
        self._send_packet(self.SERVERDATA_AUTH, self.password)
        time.sleep(0.1)
        
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
            sent_id = self._send_packet(self.SERVERDATA_EXECCOMMAND, command)
            
            # Collect all response packets
            response = ''
            while True:
                req_id, pkt_type, body = self._receive_packet()
                
                if req_id is None:
                    break
                
                # Stop when we get a response with different ID or empty body
                if req_id == sent_id and pkt_type == self.SERVERDATA_RESPONSE_VALUE:
                    response += body
                else:
                    break
            
            return response.strip()
        except Exception as e:
            print(f"Command execution error: {e}")
            return None


# Example usage
if __name__ == "__main__":
    # Configuration
    HOST = "127.0.0.1"  # Server IP
    PORT = 27015        # RCON port
    PASSWORD = "your_rcon_password"
    
    print("=" * 50)
    print("L4D2 RCON Controller")
    print("=" * 50)
    print(f"Connecting to {HOST}:{PORT}...")
    
    # Create RCON instance
    rcon = L4D2RCON(HOST, PORT, PASSWORD)
    
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

import psutil
import subprocess
import re
import time

browsers = ["chrome", "firefox", "msedge", "brave","mullvad", "safari"]

def get_network_connections(pid):
    """Retrieve remote IPs from network connections for a given PID."""
    try:
        # Use lsof to list open network connections
        result = subprocess.check_output(f"lsof -Pan -p {pid} -i", shell=True, encoding='utf-8')
        connections = []
        for line in result.splitlines():
            if "TCP" in line and "ESTABLISHED" in line:
                # Extract the remote IP using regex
                match = re.search(r'(\d+\.\d+\.\d+\.\d+):\d+', line)
                if match:
                    remote_ip = match.group(1)
                    connections.append(remote_ip)
        return connections
    except subprocess.CalledProcessError:
        return []

def resolve_ip(ip):
    """Resolve an IP address to its domain using nslookup."""
    try:
        result = subprocess.check_output(f"nslookup {ip}", shell=True, encoding='utf-8')
        for line in result.splitlines():
            if "name =" in line:
                return line.split("=")[-1].strip().rstrip(".")
    except subprocess.CalledProcessError:
        return "Unknown Host"
    return "Unknown Host"

def monitor_browser_activity():
    while True:
        for process in psutil.process_iter(['pid', 'name']):
            try:
                if any(browser in process.info['name'].lower() for browser in browsers):
                    print(f"\nBrowser Detected: {process.info['name']} (PID: {process.info['pid']})")
                    
                    # Fetch and display network connections
                    connections = get_network_connections(process.info['pid'])
                    if connections:
                        for remote_ip in connections:
                            domain_name = resolve_ip(remote_ip)
                            print(f"Remote IP: {remote_ip}, Domain: {domain_name}")
                    else:
                        print("No active network connections found.")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        time.sleep(5)  # Check every 5 seconds

if __name__ == "__main__":
    monitor_browser_activity()


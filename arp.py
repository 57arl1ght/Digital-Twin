from scapy.all import ARP, Ether, srp, conf
import requests
import time
import json
import os

STATE_FILE = "network_state.json"

def get_vendor(mac_address):
    """Gets the manufacturer name from the MAC address."""
    try:
        url = f"https://api.macvendors.com/{mac_address}"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            return response.text
        return "Uknown device"
    except requests.exceptions.RequestException:
        return "Error API"

def scan_network(ip_range):
    """Scans the network and returns a list of devices."""
    print(f"Network scan: {ip_range}...\n")
    conf.L3socket = conf.L3socket
    
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp
    
    result = srp(packet, timeout=3, verbose=0)[0]
    
    devices = {}
    for sent, received in result:
        mac = received.hwsrc
        ip = received.psrc
        devices[mac] = {'ip': ip}
    return devices

def load_state():
    """Loads the previous network state from a file."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_state(state):
    """Saves the current network state to a file."""
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
   
    previous_state = load_state()
    
    
    current_devices = scan_network("192.168.1.0/24")
    
    
    new_state = {}
    
    print("-" * 50)
    print("ANALYSIS OF CHANGES IN THE NETWORK:")
    print("-" * 50)

    
    for mac, info in current_devices.items():
        ip = info['ip']
        
        
        if mac in previous_state:
            vendor = previous_state[mac]['vendor']
            print(f"[ONLINE]  IP: {ip:<15} MAC: {mac} ({vendor})")
            new_state[mac] = {'ip': ip, 'vendor': vendor}
        
        
        else:
            print(f"[NEW!]  IP: {ip:<15} MAC: {mac} - Determining the vendor...")
            vendor = get_vendor(mac)
            print(f"          -> Manufacturer found: {vendor}")
            new_state[mac] = {'ip': ip, 'vendor': vendor}
            time.sleep(1) # Пауза для API
            

    for mac, info in previous_state.items():
        if mac not in current_devices:
            print(f"[Offline]  The device has disconnected.: MAC: {mac} ({info['vendor']})")

    # 5. Зберігаємо новий стан
    save_state(new_state)
    print("\nNetwork status saved to file 'network_state.json'")
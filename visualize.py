import json
import os
import webbrowser
from pyvis.network import Network

STATE_FILE = "network_state.json"

def generate_network_map():
    
    if not os.path.exists(STATE_FILE):
        print("The network_state.json file was not found. Run the scanner first!")
        return

   
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        devices = json.load(f)

    
    net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white", directed=False)
    
    
    net.repulsion(node_distance=150, central_gravity=0.2, spring_length=200)

    
    router_ip = None
    router_mac = None
    for mac, info in devices.items():
        if info['ip'].endswith('.1'):
            router_ip = info['ip']
            router_mac = mac
            break

    
    if router_ip:
        router_vendor = devices[router_mac].get('vendor', 'Роутер')
        net.add_node(router_mac, label=f"ШЛЮЗ\n{router_ip}\n{router_vendor}", color="#ff4d4d", size=40, shape="hexagon")
    else:
        print("Router (*.1) not found, graph may be without center.")

    
    for mac, info in devices.items():
        ip = info['ip']
        vendor = info['vendor']
        
        
        if mac == router_mac:
            continue
            
        node_label = f"{vendor}\n{ip}"
        
        
        node_color = "#00ff00" if "Micro-Star" in vendor else "#66b3ff"
        
        net.add_node(mac, label=node_label, color=node_color, size=25)
        
       
        if router_mac:
            net.add_edge(router_mac, mac, color="#555555")

    # Зберігаємо граф у HTML файл
    output_file = "network_map.html"
    net.save_graph(output_file)
    print(f"The network map has been generated! Open it {output_file}...")
    
    
    webbrowser.open('file://' + os.path.realpath(output_file))

if __name__ == "__main__":
    generate_network_map()
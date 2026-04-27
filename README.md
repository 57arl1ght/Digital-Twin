# 🌐 Network Digital Twin

A lightweight digital twin implementation for local network environments. This project focuses on the abstraction of network topology by maintaining a synchronized JSON state representation, enabling historical analysis and real-time visualization of network infrastructure.

## 🏗 Concept
This project treats the local network as a "physical" entity, where its state is captured in `network_state.json`. This JSON file acts as the **Digital Twin** — a virtual mirror that allows for visualization and analysis decoupled from real-time scan latency.

## ⚙️ Workflow
1. **Abstraction Layer (`arp.py`):** Performs network discovery to map the physical state.
2. **Twin Synchronization (`network_state.json`):** Persists the network topology, acting as the Single Source of Truth for the virtual model.
3. **Visualization Layer (`visualize.py`):** Uses an interactive graph engine to render the current "digital" state of the network.

## 🛠 Features
* **State Persistence:** Maintains a persistent virtual model of the network.
* **Topological Visualization:** Renders interactive maps based on current device connectivity.
* **Decoupled Architecture:** Separates data collection from the visualization engine.

## 🚀 How to use
1. **Sync State:** Run `python arp.py` to update the digital twin model.
2. **Visualize:** Launch `visualize.py` to open the interactive topology map in your web browser.

## ⚠️ Note
This project is intended for network topology mapping and educational digital twin modeling. Ensure compliance with local privacy regulations when scanning network environments.

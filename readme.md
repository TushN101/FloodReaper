# FloodReaper

**FloodReaper** is a powerful DDoS tool developed in Python designed to send various types of flooding and DDoS attacks. It is primarily intended for stress testing and educational purposes. Misuse of this tool for illegal activities is strictly prohibited. The author is not liable for any misuse or damage caused by this tool.

# Tool Description

This advanced network stress testing tool is designed to simulate various types of Distributed Denial of Service (DDoS) attacks, enabling users to assess the resilience and robustness of their networks. With multiple attack options available, this tool allows for comprehensive testing against potential threats, ensuring that systems can withstand various forms of malicious traffic. The tool integrates with Tornet and is configured to utilize the Tor Browser for IP hopping, enhancing anonymity during testing.
Key Features:

   # SYN Flood Attack:
        Simulates a SYN flood attack by sending a high volume of TCP SYN packets to a target, overwhelming its resources and potentially causing service disruption.

   # HTTP GET Flood Attack:
        Initiates an HTTP GET flood by sending numerous GET requests to a specified web server, testing its capacity to handle concurrent requests and identifying vulnerabilities in web applications.

   #  UDP Flood Attack:
        Executes a UDP flood attack, flooding the target with a large number of UDP packets to consume bandwidth and disrupt services.

   # Slowloris Attack:
        Implements a Slowloris attack, which keeps many connections to the target web server open and holds them open as long as possible, consuming server resources and rendering the server unable to respond to legitimate requests.

   # IP Fragmentation Attack:
        Conducts an IP fragmentation attack by sending fragmented packets to the target, potentially leading to issues in reassembling the packets and causing service interruptions.

   # DNS Amplification Attack:
        Launches a DNS amplification attack, exploiting DNS servers to flood the target with a high volume of DNS response packets, overwhelming its network bandwidth.

   # Golden Eye Attack:
        Executes a Golden Eye attack, which combines multiple techniques to maximize the impact on the target, further stressing the network and application infrastructure.

   # Tornet Integration for IP Hopping:
        Utilizes the Tornet tool alongside the Tor Browser for IP hopping, providing anonymity and obscurity during testing. This feature allows users to disguise their IP address while conducting stress tests, making it difficult to trace the origin of the attack.

Use Cases:

    Network Resilience Testing: Evaluate the robustness of networks and applications against various attack vectors.
    Security Assessment: Identify vulnerabilities and weaknesses in network infrastructure, ensuring preparedness against potential DDoS attacks.
    Performance Benchmarking: Measure how systems handle extreme traffic conditions and identify performance bottlenecks.

Disclaimer:

This tool is intended for ethical use and should only be utilized in controlled environments or with explicit permission from network owners. Unauthorized use of this tool against systems without consent is illegal and unethical.

## Installation

To install FloodReaper, follow these steps:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/TushN101/FloodReaper.git

2. **Navigate to Directory**
   ```bash
   cd FloodReaper

3. **Install Scapy**
   ```bash
   pip install scapy

4. **Run the Script**
   ```bash
   python main.py

## Legality

FloodReaper is designed for stress testing and educational purposes only. Unauthorized use of this tool for attacking networks or systems is illegal and unethical. The author is not responsible for any misuse or damage caused by this tool.

## Contributions

Contributions are welcome! If you have suggestions or improvements, please submit a pull request or open an issue.

## Author

This project is a collaborative effort by the DDoS team at DeepCytes.

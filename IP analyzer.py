import os
import subprocess
import platform
import socket
import json
import urllib.request

def clear_screen():
    """Funcție pentru curățarea ecranului terminalului."""
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def get_ip_details(ip):
    """Funcție pentru obținerea detaliilor despre adresa IP folosind serviciul ip-api.com."""
    try:
        with urllib.request.urlopen(f"http://ip-api.com/json/{ip}?fields=city,country,isp") as response:
            data = json.loads(response.read().decode())
            return data.get("city", "Unknown"), data.get("country", "Unknown"), data.get("isp", "Unknown")
    except Exception as e:
        print(f"Eroare la interogarea informațiilor IP: {e}")
        return "Unknown", "Unknown", "Unknown"

def ping_host(host):
    """Funcție pentru a verifica statusul și timpul de ping al unui host."""
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]
    
    try:
        output = subprocess.check_output(command, universal_newlines=True)
        if "TTL=" in output or "ttl=" in output:
            if platform.system().lower() == 'windows':
                ping_time = output.split('Average = ')[-1].split('ms')[0].strip() + 'ms'
            else:
                ping_time = output.split('time=')[-1].split(' ms')[0] + 'ms'
            return True, ping_time
        else:
            return False, None
    except subprocess.CalledProcessError:
        return False, None

def check_cloudflare(headers):
    """Funcție pentru a verifica dacă există header-e specifice Cloudflare."""
    if 'CF-RAY' in headers or 'cloudflare' in headers.get('server', '').lower():
        return True
    return False

def main():
    clear_screen()
    
   
    ascii_art = """
\033[91m  (   (         )               
 )\ ))\ )   ( /(               
(()/(()/(   )\())         (    
 /(_))(_)) ((_)\   (     ))\   
(_))(_))     ((_)  )\ ) /((_)  
|_ _| _ \   / _ \ _(_/((_))    
 | ||  _/  | (_) | ' \)) -_)   
|___|_|     \___/|_||_|\___|   Create By No Escape
\033[0m"""
    
    print(ascii_art)

    while True:
        ip_or_host = input("\nIntrodu adresa IP sau numele de domeniu (sau apasă Enter pentru a ieși): ").strip()
        
        if ip_or_host == "":
            break
        
        try:
            ip = socket.gethostbyname(ip_or_host)
            print(f"\nAdresa IP asociată: {ip}")
            
            city, country, isp = get_ip_details(ip)
            print(f"Locație: {city}, {country}")
            print(f"Furnizor de internet (ISP): {isp}")
            
            is_online, ping_time = ping_host(ip_or_host)
            status = "ONLINE" if is_online else "DOWN"
            ping_display = ping_time if ping_time else "N/A"
            
            if is_online:
                print("\033[92m" + f"Status: {status}")  
            else:
                print("\033[91m" + f"Status: {status}")  
            
            print(f"Ping: {ping_display}")
            
            try:
                headers = dict()
                response = urllib.request.urlopen(f"http://{ip_or_host}", timeout=5)
                for key, value in response.info().items():
                    headers[key.lower()] = value
                
                if check_cloudflare(headers):
                    print("\033[93m" + "Website-ul pare să folosească protecție de la Cloudflare.") 
                else:
                    print("\033[94m" + "Website-ul nu folosește protecție de la Cloudflare.") 

            except Exception as e:
                print(f"Eroare la verificarea header-elor HTTP: {e}")
        
        except socket.gaierror:
            print(f"Eroare: Nu am putut rezolva numele de domeniu '{ip_or_host}' într-o adresă IP.")

        input("\nApasă Enter pentru a continua...")

if __name__ == "__main__":
    main()

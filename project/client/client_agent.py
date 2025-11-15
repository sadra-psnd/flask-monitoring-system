import requests
import time
import json
import platform
from metrics import get_network_speeds, packet_loss, uptime_calculator, plugged_status
import psutil
import datetime

class SystemMonitor:
    def __init__(self, server_url, client_id=None):
        self.server_url = server_url
        self.client_id = client_id or f"{platform.node()}-{platform.system()}"
        
    def collect_system_data(self):
        upload, download = get_network_speeds()
        
        data = {
            'client_id': self.client_id,
            'hostname': platform.node(),
            'cpu': psutil.cpu_percent(),
            'ram': psutil.virtual_memory().percent,
            'disk': psutil.disk_usage('/').percent, 
            'processes': len(psutil.pids()),
            'upload': upload,
            'download': download,
            'boot_time': datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"),
            'num_cpu_physical_core': psutil.cpu_count(logical=False),
            'uptime': uptime_calculator(),
            'cpu_info': platform.processor(),
            'cpu_current_freq': psutil.cpu_freq().current if psutil.cpu_freq() else None,
            'total_RAM': round(psutil.virtual_memory().total / (1024**3)),
            'ava_RAM': psutil.virtual_memory().available,
            'packetloss': packet_loss(count=5),  # Reduced count for faster reporting
            'battery_percent': psutil.sensors_battery().percent if psutil.sensors_battery() else None,
            'plugged_state': plugged_status()
        }
        return data
    
    def send_data_to_server(self):
        data = self.collect_system_data()
        try:
            response = requests.post(
                f"{self.server_url}/api/submit_stats",
                json=data,
                timeout=10
            )
            if response.status_code == 200:
                print(f"Data sent successfully at {datetime.datetime.now()}")
            else:
                print(f"Failed to send data: {response.status_code}")
        except Exception as e:
            print(f"Error sending data: {e}")
    
    def run(self, interval=60):
        """Run the monitoring agent"""
        print(f"Starting system monitor for client: {self.client_id}")
        print(f"Reporting to: {self.server_url}")
        print(f"Interval: {interval} seconds")
        print("Press Ctrl+C to stop...")
        
        try:
            while True:
                self.send_data_to_server()
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\nMonitoring stopped.")

if __name__ == "__main__":
    # Configuration - UPDATE THIS URL FOR YOUR SERVER
<<<<<<< HEAD
    SERVER_URL = "http://192.168.1.100:5000"  # Change to your server IP
    MONITOR = SystemMonitor(SERVER_URL)
    MONITOR.run(interval=60)  # Report every 60 seconds
=======
    SERVER_URL = "http://192.168.168.137:5000"  # Change to your server IP
    MONITOR = SystemMonitor(SERVER_URL)
    MONITOR.run(interval=60)  # Report every 60 seconds
>>>>>>> master

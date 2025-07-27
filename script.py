import platform
import psutil
import socket
import uuid
import os
import subprocess
from datetime import datetime
import json

def get_system_info():
    uname = platform.uname()
    svmem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    net_if_addrs = psutil.net_if_addrs()

    cpu_info = {
        "Physical cores": psutil.cpu_count(logical=False),
        "Total cores": psutil.cpu_count(logical=True),
        "Max Frequency (MHz)": psutil.cpu_freq().max,
        "Min Frequency (MHz)": psutil.cpu_freq().min,
        "Current Frequency (MHz)": psutil.cpu_freq().current,
        "CPU Usage (%)": psutil.cpu_percent(interval=1),
    }

    ram_info = {
        "Total Memory (GB)": round(svmem.total / (1024 ** 3), 2),
        "Available Memory (GB)": round(svmem.available / (1024 ** 3), 2),
        "Used Memory (GB)": round(svmem.used / (1024 ** 3), 2),
        "Memory Usage (%)": svmem.percent,
    }

    disk_info = {
        "Total Disk Space (GB)": round(disk.total / (1024 ** 3), 2),
        "Used Disk Space (GB)": round(disk.used / (1024 ** 3), 2),
        "Free Disk Space (GB)": round(disk.free / (1024 ** 3), 2),
        "Disk Usage (%)": disk.percent,
    }

    net_info = []
    for interface, addresses in net_if_addrs.items():
        for addr in addresses:
            if addr.family == socket.AF_INET:
                net_info.append({
                    "Interface": interface,
                    "IP Address": addr.address,
                    "Netmask": addr.netmask,
                    "Broadcast IP": addr.broadcast,
                })

    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    uptime = str(datetime.now() - bt).split('.')[0]

    other_info = {
        "OS": uname.system,
        "OS Version": uname.version,
        "OS Release": uname.release,
        "Machine": uname.machine,
        "Processor": uname.processor,
        "Hostname": socket.gethostname(),
        "IP Address": socket.gethostbyname(socket.gethostname()),
        "MAC Address": ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0, 8 * 6, 8)][::-1]),
        "UUID": str(uuid.uuid4()),
        "Uptime": uptime,
        "Python Version": platform.python_version(),
        "Shell": os.environ.get('SHELL', 'N/A')
    }

    try:
        gpu_info = subprocess.check_output("lshw -C display | grep 'product'", shell=True).decode().strip()
    except Exception:
        gpu_info = "GPU Info Not Found"

    system_info = {
        "CPU Info": cpu_info,
        "RAM Info": ram_info,
        "Disk Info": disk_info,
        "Network Interfaces": net_info,
        "Other Info": other_info,
        "GPU Info": gpu_info
    }

    return system_info

if __name__ == "__main__":
    info = get_system_info()
    with open("system_info.json", "w") as f:
        json.dump(info, f, indent=4)
    print("System information saved to system_info.json")

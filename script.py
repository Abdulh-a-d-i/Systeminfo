import platform
import psutil
import socket
import uuid
import os
import json

def get_system_info():
    uname = platform.uname()
    svmem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    # Network Info (Interface enp0s3)
    enp0s3_ip = None
    net_if_addrs = psutil.net_if_addrs()
    if 'enp0s3' in net_if_addrs:
        for addr in net_if_addrs['enp0s3']:
            if addr.family == socket.AF_INET:
                enp0s3_ip = addr.address

    system_info = {
        "OS": uname.system,
        "OS Version": uname.version,
        "OS Release": uname.release,
        "Hostname": socket.gethostname(),
        "Machine Architecture": uname.machine,
        "MAC Address": ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0, 8 * 6, 8)][::-1]),
        "enp0s3 IP": enp0s3_ip if enp0s3_ip else "Not Found",
        "Disk Info": {
            "Total (GB)": round(disk.total / (1024 ** 3), 2),
            "Used (GB)": round(disk.used / (1024 ** 3), 2),
            "Free (GB)": round(disk.free / (1024 ** 3), 2),
            "Usage (%)": disk.percent,
        },
        "Total RAM (GB)": round(svmem.total / (1024 ** 3), 2),
        "CPU Cores": {
            "Physical": psutil.cpu_count(logical=False),
            "Logical": psutil.cpu_count(logical=True),
        }
    }

    return system_info

if __name__ == "__main__":
    info = get_system_info()
    with open("system_info.json", "w") as f:
        json.dump(info, f, indent=4)
    print("System information saved to system_info.json")

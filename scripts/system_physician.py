import psutil
import json
import time

def get_system_health():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    health_report = {
        "node": "The Alpha Node",
        "timestamp": int(time.time()),
        "status": "Healthy",
        "metrics": {
            "cpu_usage_percent": cpu_usage,
            "memory_available_gb": round(memory.available / (1024**3), 2),
            "memory_used_percent": memory.percent,
            "disk_free_gb": round(disk.free / (1024**3), 2)
        }
    }
    
    return health_report

if __name__ == "__main__":
    print(json.dumps(get_system_health(), indent=2))

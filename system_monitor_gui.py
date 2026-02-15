import psutil
import tkinter as tk
from tkinter import ttk
import os

# GPU
try:
    import GPUtil
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False


def bytes_to_gb(value):
    return round(value / (1024 ** 3), 2)


def get_cpu_temperature():
    try:
        temps = psutil.sensors_temperatures()
        if not temps:
            return "Немає датчика"
        for name, entries in temps.items():
            for entry in entries:
                if entry.current:
                    return f"{entry.current} °C"
        return "Немає датчика"
    except:
        return "Недоступно"


def get_gpu_info():
    if not GPU_AVAILABLE:
        return None
    try:
        gpus = GPUtil.getGPUs()
        if not gpus:
            return None
        gpu = gpus[0]
        return {
            "name": gpu.name,
            "load": round(gpu.load * 100, 1),
            "memory_used": round(gpu.memoryUsed / 1024, 2),
            "memory_total": round(gpu.memoryTotal / 1024, 2),
            "temperature": f"{gpu.temperature} °C"
        }
    except:
        return None


def update_data():
    # CPU
    cpu_usage.set(f"{psutil.cpu_percent()} %")
    cpu_temp.set(get_cpu_temperature())

    # RAM
    memory = psutil.virtual_memory()
    total_ram.set(f"{bytes_to_gb(memory.total)} GB")
    used_ram.set(f"{bytes_to_gb(memory.used)} GB")
    free_ram.set(f"{bytes_to_gb(memory.available)} GB")

    # GPU
    gpu_info = get_gpu_info()
    if gpu_info:
        gpu_name.set(gpu_info["name"])
        gpu_load.set(f"{gpu_info['load']} %")
        gpu_mem.set(f"{gpu_info['memory_used']} / {gpu_info['memory_total']} GB")
        gpu_temp.set(gpu_info["temperature"])
    else:
        gpu_name.set("Немає або недоступна")
        gpu_load.set("-")
        gpu_mem.set("-")
        gpu_temp.set("-")

    root.after(1000, update_data)


# ---------------- GUI ----------------

root = tk.Tk()
root.title("Система моніторингу ПК")
root.geometry("500x400")
root.resizable(False, False)

style = ttk.Style()
style.configure("TLabel", font=("Arial", 11))

main_frame = ttk.Frame(root, padding=20)
main_frame.pack(fill="both", expand=True)

# Змінні
cpu_usage = tk.StringVar()
cpu_temp = tk.StringVar()

total_ram = tk.StringVar()
used_ram = tk.StringVar()
free_ram = tk.StringVar()

gpu_name = tk.StringVar()
gpu_load = tk.StringVar()
gpu_mem = tk.StringVar()
gpu_temp = tk.StringVar()

# CPU
ttk.Label(main_frame, text="CPU", font=("Arial", 14, "bold")).pack(anchor="w")
ttk.Label(main_frame, textvariable=cpu_usage).pack(anchor="w")
ttk.Label(main_frame, textvariable=cpu_temp).pack(anchor="w")

ttk.Separator(main_frame).pack(fill="x", pady=10)

# RAM
ttk.Label(main_frame, text="RAM", font=("Arial", 14, "bold")).pack(anchor="w")
ttk.Label(main_frame, text="Загальна:").pack(anchor="w")
ttk.Label(main_frame, textvariable=total_ram).pack(anchor="w")
ttk.Label(main_frame, text="Використано:").pack(anchor="w")
ttk.Label(main_frame, textvariable=used_ram).pack(anchor="w")
ttk.Label(main_frame, text="Вільно:").pack(anchor="w")
ttk.Label(main_frame, textvariable=free_ram).pack(anchor="w")

ttk.Separator(main_frame).pack(fill="x", pady=10)

# GPU
ttk.Label(main_frame, text="GPU", font=("Arial", 14, "bold")).pack(anchor="w")
ttk.Label(main_frame, text="Назва:").pack(anchor="w")
ttk.Label(main_frame, textvariable=gpu_name).pack(anchor="w")
ttk.Label(main_frame, text="Завантаження:").pack(anchor="w")
ttk.Label(main_frame, textvariable=gpu_load).pack(anchor="w")
ttk.Label(main_frame, text="Памʼять:").pack(anchor="w")
ttk.Label(main_frame, textvariable=gpu_mem).pack(anchor="w")
ttk.Label(main_frame, text="Температура:").pack(anchor="w")
ttk.Label(main_frame, textvariable=gpu_temp).pack(anchor="w")

update_data()
root.mainloop()
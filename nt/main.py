import tkinter as tk
from tkinter import messagebox, ttk
from ttkthemes import ThemedTk
import socket
import subprocess
import platform
import psutil

def check_open_ports():
    ip = entry_ip.get()
    ports = [80, 443, 21, 22, 23, 25, 53, 110, 143, 3306, 3389]
    open_ports = []
   
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
   
    if open_ports:
        messagebox.showinfo("Open Ports", f"Open ports on {ip}: {', '.join(map(str, open_ports))}")
    else:
        messagebox.showinfo("Open Ports", f"No open ports found on {ip}")

def scan_network():
    network = entry_network.get()
    cmd = ["nmap", "-sn", "-Pn", network]
    result = subprocess.run(cmd, capture_output=True, text=True)
    messagebox.showinfo("Network Scan", result.stdout)

def check_server_status():
    server = entry_server.get()
    try:
        response = subprocess.check_output(["ping", "-n", "1", server])
        messagebox.showinfo("Server Status", f"{server} is reachable")
    except subprocess.CalledProcessError:
        messagebox.showinfo("Server Status", f"{server} is not reachable")

def detect_os():
    ip = entry_ip.get()
    cmd = ["nmap", "-O", ip]
    result = subprocess.run(cmd, capture_output=True, text=True)
    messagebox.showinfo("OS Detection", result.stdout)

def traceroute():
    ip = entry_ip.get()
    cmd = ["tracert", ip]
    result = subprocess.run(cmd, capture_output=True, text=True)
    messagebox.showinfo("Traceroute", result.stdout)

def check_vulnerabilities():
    ip = entry_ip.get()
    cmd = ["nmap", "--script", "vuln", ip]
    result = subprocess.run(cmd, capture_output=True, text=True)
    messagebox.showinfo("Vulnerability Scan", result.stdout)

def system_info():
    info = f"System: {platform.system()}\n"
    info += f"Node Name: {platform.node()}\n"
    info += f"Release: {platform.release()}\n"
    info += f"Version: {platform.version()}\n"
    info += f"Machine: {platform.machine()}\n"
    info += f"Processor: {platform.processor()}\n"
    messagebox.showinfo("System Info", info)

def find_hosts():
    network = entry_network_additional.get()
    cmd = ["nmap", "-sn", "-Pn", network]
    result = subprocess.run(cmd, capture_output=True, text=True)
    messagebox.showinfo("Hosts in Network", result.stdout)

def save_settings():
    ip = entry_ip.get()
    network = entry_network.get()
    server = entry_server.get()
    theme = combobox_theme.get()
   
    settings = f"IP: {ip}\nNetwork: {network}\nServer: {server}\nTheme: {theme}"
   
    with open("settings.txt", "w") as file:
        file.write(settings)
   
    messagebox.showinfo("Settings Saved", "Settings have been saved successfully.")

def change_theme():
    theme = combobox_theme.get()
    root.set_theme(theme)
    messagebox.showinfo("Theme Changed", f"Theme changed to {theme}")

def monitor_resources():
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    ram_usage = psutil.virtual_memory().used / (1024 ** 3)  # RAM w GB
    messagebox.showinfo("Resource Monitor", f"CPU Usage: {cpu_usage}%\nMemory Usage: {memory_usage}%\nDisk Usage: {disk_usage}%\nRAM Usage: {ram_usage:.2f} GB")

# Tworzenie głównego okna aplikacji
root = ThemedTk(theme="breeze")
root.title("NETWORK TOOL")
root.geometry("600x500")
root.configure(bg='#f0f0f0')  # Ustawienie koloru tła dla okna głównego

# Nagłówek
label_title = ttk.Label(root, text="NETWORK TOOL", font=("Helvetica", 18, "bold"), foreground='#4a4e69', background='#f0f0f0')
label_title.pack(pady=8)

# Tworzenie zakładek
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

# Zakładka 1: Skanowanie
frame_scan = ttk.Frame(notebook)
notebook.add(frame_scan, text="Scan")


label_ip = ttk.Label(frame_scan, text="\nEnter IP address:")
label_ip.pack(pady=10)
entry_ip = ttk.Entry(frame_scan)
entry_ip.pack(pady=5)

label_network = ttk.Label(frame_scan, text="Enter network (e.g., 192.168.1.0/24):")
label_network.pack(pady=10)
entry_network = ttk.Entry(frame_scan)
entry_network.pack(pady=5)

label_server = ttk.Label(frame_scan, text="Enter server address:")
label_server.pack(pady=10)
entry_server = ttk.Entry(frame_scan)
entry_server.pack(pady=5)

button_ports = ttk.Button(frame_scan, text="Check Open Ports", command=check_open_ports)
button_ports.pack(pady=5)

button_network = ttk.Button(frame_scan, text="Scan Network", command=scan_network)
button_network.pack(pady=5)

button_server = ttk.Button(frame_scan, text="Check Server Status", command=check_server_status)
button_server.pack(pady=5)

# Zakładka 2: Analiza
frame_analysis = ttk.Frame(notebook)
notebook.add(frame_analysis, text="Analysis")


button_os = ttk.Button(frame_analysis, text="Detect OS", command=detect_os)
button_os.pack(pady=(30, 5))

button_traceroute = ttk.Button(frame_analysis, text="Traceroute", command=traceroute)
button_traceroute.pack(pady=5)

button_vulnerabilities = ttk.Button(frame_analysis, text="Check Vulnerabilities", command=check_vulnerabilities)
button_vulnerabilities.pack(pady=5)

button_system_info = ttk.Button(frame_analysis, text="System Info", command=system_info)
button_system_info.pack(pady=5)

# Zakładka 3: Dodatkowe funkcje
frame_additional = ttk.Frame(notebook)
notebook.add(frame_additional, text="Additional Functions")

label_network_additional = ttk.Label(frame_additional,  font=10, text="\n\nEnter network (e.g., 192.168.1.0/24):")
label_network_additional.pack(pady=10)
entry_network_additional = ttk.Entry(frame_additional)
entry_network_additional.pack(pady=5)

button_find_hosts = ttk.Button(frame_additional, text="Find Hosts in Network", command=find_hosts)
button_find_hosts.pack(pady=5)

# Zakładka 4: Monitorowanie zasobów
frame_resource_monitoring = ttk.Frame(notebook)
notebook.add(frame_resource_monitoring, text="Resource Monitoring")

label_cpu = ttk.Label(frame_resource_monitoring, text="CPU Usage:")
label_cpu.grid(row=0, column=0, padx=250, pady=5)
label_memory = ttk.Label(frame_resource_monitoring, text="Memory Usage:")
label_memory.grid(row=1, column=0, padx=200, pady=5)
label_disk = ttk.Label(frame_resource_monitoring, text="Disk Usage:")
label_disk.grid(row=2, column=0, padx=200, pady=5)
label_ram = ttk.Label(frame_resource_monitoring, text="RAM Usage:")
label_ram.grid(row=3, column=0, padx=200, pady=5)

def update_resource_usage():
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    ram_usage = psutil.virtual_memory().used / (1024 ** 3)  # RAM w GB
   
    label_cpu.config(text=f"\n\nCPU Usage: {cpu_usage}%")
    label_memory.config(text=f"Memory Usage: {memory_usage}%")
    label_disk.config(text=f"Disk Usage: {disk_usage}%")
    label_ram.config(text=f"RAM Usage: {ram_usage:.2f} GB")

    # Ponowne uruchomienie funkcji po 1000 ms
    root.after(1000, update_resource_usage)

# Uruchomienie funkcji monitorowania zasobów po raz pierwszy
update_resource_usage()


# Zakładka 3: Ustawienia
frame_settings = ttk.Frame(notebook)
notebook.add(frame_settings, text="Settings")

label_theme = ttk.Label(frame_settings, font=10, text="\nSelect Theme:")

label_theme.pack(pady=10)
themes = ["breeze", "arc", "clearlooks", "equilux", "keramik", "plastik", "radiance", "scidblue"]
combobox_theme = ttk.Combobox(frame_settings, values=themes)
combobox_theme.pack(pady=5)
combobox_theme.current(0)

button_save_settings = ttk.Button(frame_settings, text="Save Settings", command=save_settings)
button_save_settings.pack(pady=5)

button_change_theme = ttk.Button(frame_settings, text="Change Theme", command=change_theme)
button_change_theme.pack(pady=5)

# Uruchomienie pętli głównej
root.mainloop()

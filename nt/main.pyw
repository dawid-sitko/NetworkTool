import tkinter as tk
from tkinter import messagebox, ttk
from ttkthemes import ThemedTk
import socket
import subprocess
import platform
import psutil
import re

def check_open_ports():
    ip = entry_ip.get()
    ports = [80, 443, 21, 22, 23, 25, 53, 110, 143, 3306, 3389]
    open_ports = []
   
    try:
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

    except socket.gaierror as e:
        messagebox.showerror("Error", f"Failed to connect to {ip}: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

def scan_network():
    network = entry_network.get().strip()
    
    if not network:
        messagebox.showerror("Input Error", "Please enter a network range.")
        return

    cmd = ["nmap", "-Pn", network]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        output = result.stdout
        messagebox.showinfo("Network Scan", output)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while scanning the network:\n{e}")

def check_server_status():
    server = entry_server.get().strip()
    
    if not server:
        messagebox.showerror("Input Error", "Please enter a server address.")
        return
    
    try:
        response = subprocess.check_output(["ping", "-n", "1", server], stderr=subprocess.STDOUT, universal_newlines=True)
        messagebox.showinfo("Server Status", f"{server} is reachable")
    except subprocess.CalledProcessError:
        messagebox.showinfo("Server Status", f"{server} is unreachable")

def detect_os():
    ip = entry_ip.get().strip()
    
    if not ip:
        messagebox.showerror("Input Error", "Please enter an IP address.")
        return
    
    try:
        response = subprocess.check_output(["ping", "-n", "1", ip], stderr=subprocess.STDOUT, universal_newlines=True)
        if "TTL=" in response:
            if "TTL=64" in response:
                os_type = "Linux or Unix-like"
            else:
                os_type = "Windows"
        else:
            os_type = "Unknown"

        messagebox.showinfo("Detecting Operating System", f"Operating system on {ip}: {os_type}")
    
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", f"Failed to get a response from {ip}")

def traceroute():
    ip = entry_ip.get().strip()
    
    if not ip:
        messagebox.showerror("Input Error", "Please enter an IP address.")
        return
    
    cmd = ["tracert", ip]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        output = result.stdout
        messagebox.showinfo("Traceroute", output)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during traceroute:\n{e}")

def check_vulnerabilities():
    ip = entry_ip.get().strip()
    
    if not ip:
        messagebox.showerror("Input Error", "Please enter an IP address.")
        return
    
    cmd = ["nmap", "--script", "vuln", ip]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        output = result.stdout
        messagebox.showinfo("Checking Vulnerabilities", output)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while checking vulnerabilities:\n{e}")

def system_info():
    info = f"System: {platform.system()}\n"
    info += f"Hostname: {platform.node()}\n"
    info += f"Version: {platform.version()}\n"
    info += f"Machine: {platform.machine()}\n"
    info += f"Processor: {platform.processor()}\n"
    messagebox.showinfo("System Information", info)

def find_hosts():
    network = entry_network_additional.get().strip()
    
    if not network:
        messagebox.showerror("Input Error", "Please enter a network range.")
        return
    
    cmd = ["nmap", "-sn", network]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        output = result.stdout
        
        if "0 hosts up" in output:
            messagebox.showinfo("Network Devices", "No devices found. Make sure the network range is correct and devices are reachable.")
        else:
            messagebox.showinfo("Network Devices", output)
    
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while scanning the network:\n{e}")

def save_settings():
    ip = entry_ip.get().strip()
    network = entry_network.get().strip()
    server = entry_server.get().strip()
    theme = combobox_theme.get()
   
    settings = f"IP: {ip}\nNetwork: {network}\nServer: {server}\nTheme: {theme}"
   
    try:
        with open("settings.txt", "w") as file:
            file.write(settings)
        messagebox.showinfo("Settings Saved", "Settings saved successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving settings:\n{e}")

def change_theme():
    theme = combobox_theme.get()
    try:
        root.set_theme(theme)
        messagebox.showinfo("Theme Changed", f"Theme changed to {theme}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while changing the theme:\n{e}")

def monitor_resources():
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    ram_usage = psutil.virtual_memory().used / (1024 ** 3)  # RAM in GB
    messagebox.showinfo("Resource Monitoring", f"CPU Usage: {cpu_usage}%\nMemory Usage: {memory_usage}%\nDisk Usage: {disk_usage}%\nRAM Usage: {ram_usage:.2f} GB")

def update_resource_usage():
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    ram_usage = psutil.virtual_memory().used / (1024 ** 3)  # RAM in GB
   
    label_cpu.config(text=f"\n\nCPU Usage: {cpu_usage}%")
    label_memory.config(text=f"Memory Usage: {memory_usage}%")
    label_disk.config(text=f"Disk Usage: {disk_usage}%")
    label_ram.config(text=f"RAM Usage: {ram_usage:.2f} GB")

    # Restart the function after 1000 ms
    root.after(1000, update_resource_usage)

# Creating the main application window
root = ThemedTk(theme="breeze")
root.title("NETWORK TOOL")
root.geometry("600x500")
root.configure(bg='#f0f0f0')  # Set background color for the main window

# Header
label_title = ttk.Label(root, text="NETWORK TOOL", font=("Helvetica", 18, "bold"), foreground='#4a4e69', background='#f0f0f0')
label_title.pack(pady=8)

# Creating tabs
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

# Tab 1: Scanning
frame_scan = ttk.Frame(notebook)
notebook.add(frame_scan, text="Scanning")

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

# Tab 2: Analysis
frame_analysis = ttk.Frame(notebook)
notebook.add(frame_analysis, text="Analysis")

button_os = ttk.Button(frame_analysis, text="Detect Operating System", command=detect_os)
button_os.pack(pady=(30, 5))

button_traceroute = ttk.Button(frame_analysis, text="Traceroute", command=traceroute)
button_traceroute.pack(pady=5)

button_vulnerabilities = ttk.Button(frame_analysis, text="Check Vulnerabilities", command=check_vulnerabilities)
button_vulnerabilities.pack(pady=5)

button_system_info = ttk.Button(frame_analysis, text="System Information", command=system_info)
button_system_info.pack(pady=5)

# System Information
button_system_info = ttk.Button(frame_analysis, text="System Information", command=system_info)
button_system_info.pack(pady=5)

# Tab 3: Additional Functions
frame_additional = ttk.Frame(notebook)
notebook.add(frame_additional, text="Additional Functions")

label_network_additional = ttk.Label(frame_additional, text="\nEnter network (e.g., 192.168.1.0/24):")
label_network_additional.pack(pady=10)
entry_network_additional = ttk.Entry(frame_additional)
entry_network_additional.pack(pady=5)

button_find_hosts = ttk.Button(frame_additional, text="Find Devices in Network", command=find_hosts)
button_find_hosts.pack(pady=5)

# Tab 4: Resource Monitoring
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

# Tab 5: Settings
frame_settings = ttk.Frame(notebook)
notebook.add(frame_settings, text="Settings")

label_theme = ttk.Label(frame_settings, text="\nSelect theme:")
label_theme.pack(pady=10)

themes = ["breeze", "arc", "clearlooks", "equilux", "keramik", "plastik", "radiance", "scidblue"]
combobox_theme = ttk.Combobox(frame_settings, values=themes)
combobox_theme.pack(pady=5)
combobox_theme.current(0)

button_save_settings = ttk.Button(frame_settings, text="Save Settings", command=save_settings)
button_save_settings.pack(pady=5)

button_change_theme = ttk.Button(frame_settings, text="Change Theme", command=change_theme)
button_change_theme.pack(pady=5)

# Start resource monitoring function initially
update_resource_usage()

# Start the main loop
root.mainloop()

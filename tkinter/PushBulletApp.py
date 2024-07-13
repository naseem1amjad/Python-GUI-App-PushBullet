import tkinter as tk
from tkinter import filedialog
import time
import pushbullet

# Connect to Pushbullet API
def connect_api():
    global pb
    api_key = api_key_entry.get()
    pb = pushbullet.Pushbullet(api_key)
    status_label.config(text="API Connected", fg="green")
    device_dropdown.config(state="normal")

# Choose the device to send the message from
def choose_device():
    global device
    device = devices[device_dropdown.current()]
    status_label.config(text="Device Selected: "+device.nickname, fg="green")
    message_button.config(state="normal")

# Choose the message file
def choose_file():
    global message
    message_file = filedialog.askopenfilename()
    with open(message_file) as file:
        message = file.read()
    status_label.config(text="Message File Loaded", fg="green")
    send_button.config(state="normal")

# Send the message
def send_message():
    global send_count
    send_count = 0
    interval = int(interval_entry.get())
    status_label.config(text="Message Sending...", fg="blue")
    while True:
        try:
            push = pb.push_note(device_iden=device.device_iden, title="Message", body=message)
            print("Message sent at", time.strftime("%H:%M:%S"))
            send_count += 1
            time.sleep(interval)
        except:
            status_label.config(text="Error Sending Message", fg="red")
            break

# Create the GUI
root = tk.Tk()
root.title("Pushbullet Message Sender")
root.geometry("320x400")

# API Key input
api_key_label = tk.Label(root, text="API Key:")
api_key_label.pack()
api_key_entry = tk.Entry(root)
api_key_entry.pack()

# Connect button
connect_button = tk.Button(root, text="Connect", command=connect_api)
connect_button.pack()

# Device dropdown
device_label = tk.Label(root, text="Select Device:")
device_label.pack()
device_dropdown = tk.OptionMenu(root, tk.StringVar(), "")
device_dropdown.config(state="disabled")
device_dropdown.pack()

# Message input
message_label = tk.Label(root, text="Select Message File:")
message_label.pack()
message_button = tk.Button(root, text="Choose File", command=choose_file)
message_button.config(state="disabled")
message_button.pack()

# Transmission interval input
interval_label = tk.Label(root, text="Transmission Interval (seconds):")
interval_label.pack()
interval_entry = tk.Entry(root)
interval_entry.pack()

# Start button
send_button = tk.Button(root, text="Start", command=send_message)
send_button.config(state="disabled")
send_button.pack()

# Status label
status_label = tk.Label(root, text="Ready", fg="black")
status_label.pack()

# Load devices
try:
    api_key = api_key_entry.get()
    pb = pushbullet.Pushbullet(api_key)
    devices = pb.devices
    device_names = [device.nickname for device in devices]
    device_dropdown['menu'].delete(0, 'end')
    for name in device_names:
        device_dropdown['menu'].add_command(label=name, command=choose_device)
except:
    pass

root.mainloop()

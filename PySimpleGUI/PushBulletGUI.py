import PySimpleGUI as sg
import pushbullet
from datetime import datetime


# Load configuration information from file
with open('config.txt', 'r') as f:
    config = f.read().splitlines()
    api_key = config[0]
    time_interval = int(config[1])

# Connect to Pushbullet API
pb = pushbullet.Pushbullet(api_key)

# Get list of devices
devices = pb.devices

# Set up GUI layout
layout = [
    [sg.Text('Select Device:')],
    [sg.Combo(devices, size=(30, 1), key='-DEVICE-', enable_events=True)],
    [sg.Text('Select Message File:')],
    [sg.Input(key='-MESSAGE-'), sg.FileBrowse()],
    [sg.Text('Transmission Time Interval (Seconds):')],
    [sg.Slider(range=(1, 60), default_value=time_interval, size=(40, 10), key='-INTERVAL-', enable_events=True, orientation='h')],
    [sg.Button('Start', disabled=True), sg.Button('Stop'), sg.Button('Exit')],
    [sg.StatusBar(text='Ready', size=(40, 1), key='-STATUS-')],
]

# Create the window
window = sg.Window('Pushbullet App', layout)

# Main event loop
send_loop_running = False
while True:
    event, values = window.read(timeout=100)

    # If the window is closed, exit the program
    if event in (sg.WIN_CLOSED, 'Exit'):
        break

    # If the user selects a device, enable the Start button
    if event == '-DEVICE-':
        window['Start'].update(disabled=False)

    # If the user changes the time interval, update the interval variable
    if event == '-INTERVAL-':
        time_interval = int(values['-INTERVAL-'])

    # If the user clicks the Start button, start the send loop
    if event == 'Start':
        send_loop_running = True
        window['Start'].update(disabled=True)
        window['Stop'].update(disabled=False)
        window['-STATUS-'].update('Loop Started')
        device = values['-DEVICE-']
        device=str(device).split("(")[1].split(")")[0]

        message_file = values['-MESSAGE-']
        with open(message_file, 'r') as f:
            message = f.read()
        while send_loop_running:
            pb.push_note(f'Message from {device}', message)
            print(f"Message sent at {datetime.now().strftime('%H:%M:%S')}")
            window.refresh()
            event, values = window.read(timeout=time_interval*1000)
            if event == 'Stop':
                send_loop_running = False

    # If the user clicks the Stop button, stop the send loop
    if event == 'Stop':
        send_loop_running = False
        window['Start'].update(disabled=False)
        window['Stop'].update(disabled=True)
        window['-STATUS-'].update('Loop Stopped')

# Close the window
window.close()

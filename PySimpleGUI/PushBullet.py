import pushbullet
import time

# Load configuration information from file
with open('config.txt', 'r') as f:
    config = f.read().splitlines()
    api_key = config[0]
    access_token= api_key
    time_interval = int(config[1])
    
pb = pushbullet.Pushbullet(api_key, access_token)

# Choose the device
devices = pb.devices
print('Choose the device to send messages from:')
for i, device in enumerate(devices):
    print(f'{i}: {device.nickname}')
index = int(input())
device = devices[index]

# Choose the message content
filename = input('Enter the path to the file containing the message: ')
with open(filename, 'r') as f:
    message = f.read()

# Set the time interval
interval = int(input('Enter the time interval (in seconds) between each transmission: '))

# Send the messages automatically
print('Sending messages...')
while True:
    try:
        push = pb.push_note(f'Message from {device.nickname}', message, device=device)
        print(f'Message sent at {time.strftime("%Y-%m-%d %H:%M:%S")}')
        time.sleep(interval)
    except KeyboardInterrupt:
        print('Transmission stopped by user.')
        break

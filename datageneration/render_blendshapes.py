# Added VRCFT blendshapes to Mesh in RenderSceneV2.blend, ready to write
import bpy
import math
import random
import socket
import pickle
import struct

def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data


HOST = 'localhost'
PORT = 50000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

while True:
    conn, (address, port) = s.accept()
    data = recv_msg(conn)
    render_job = pickle.loads(data)
    print(f'Got: {render_job[0]}')
    ack_msg = pickle.dumps('Got Blendshape Lists')
    send_msg(conn, ack_msg)
    ack_msg = pickle.dumps('Rendering')
    send_msg(conn, ack_msg)




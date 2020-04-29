#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'
PORT = 12001

ACK = 'acknowledged'


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen()
    conn, addr = sock.accept()

    #EMPTY THIS STRING BEFORE COMMITING
    #order of details in string: "receiver_text sender_text sender_password"
    message = ""
    sendText(message, conn)

def sendText(message, sock):
    # encode the text message
    encodedMessage = bytes(message, 'utf-8')

    #Send exfiltration details
    sock.sendall(encodedMessage)

    #receive ACK
    encodedAckText = sock.recv(1024)
    ackText = encodedAckText.decode('utf-8')

    #Print error if acknowledge was not successful
    if ackText == ACK:
        print('server acknowledged reception of text')
    else:
        print('error: server has sent back ' + ackText)

main()

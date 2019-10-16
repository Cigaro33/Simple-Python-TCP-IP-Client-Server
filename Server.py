import socket
import sys
import config
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from random import seed
from random import randint
import os.path

value1 = randint(10000, 90000)
val= str(value1)
body = val
subject = "Email via Python"

msg = MIMEMultipart()
msg['From'] = config.mailFromAdress
msg['To'] = config.mailToAdress
msg['Subject'] = subject
msg.attach(MIMEText(body,'plain'))
message = msg.as_string()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Bind the socket to the port
server_address = ('192.168.1.24', 10000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)
# Listen for incoming connections
sock.listen(1)

while True:
    connection, client_address = sock.accept()
    print >>sys.stderr, 'waiting for a connection'

    # Wait for a connection

    try:
        #print client_address
        #label .start
        if os.path.exists('UP.txt')==False:
            connection.sendall("Sei nuovo, vuoi creare un account?(y/n) ")
            scel=connection.recv(15)
            if scel=='y':
                connection.sendall("Sto mandando un email con un codice di registrazione...")
                atte=connection.recv(15)
                try:
                    server = smtplib.SMTP(config.mailFromServer)
                    server.starttls()
                    server.login(config.mailFromAdress, config.mailFromPassword)

                    server.sendmail(config.mailFromAdress, config.mailToAdress, message)
                    server.quit()
                    connection.sendall("SUCCESS - Email sent, inserisci il codice ricevuto: ")
                    cod=connection.recv(15)
                    if cod == val:
                        i=open('UP.txt','w')
                        connection.sendall("Codice corretto, crea username e password: ")
                        up=connection.recv(15)
                        isc=i.write(up)
                        connection.sendall("Operazione terminata con successo!")
                    else:
                        connection.sendall("Codice errato")
                        exit()
                except Exception as e:
                    print("FAILURE - Email not sent")
                    print(e)
                    exit()
            else:
                connection.sendall("Impossibile proseguire senza una registrazione")
                exit()
        a=open('UP.txt','r').readline()
        connection.sendall("Inserisci Username e Password: ")
        ps = connection.recv(15)
        #ps=ps+'\n'
        if ps==a:
            connection.sendall("Connection accepted")
        else:
            connection.sendall("Connection refused")
            break
            #goto .start
        print >>sys.stderr, 'connection from', client_address
        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(15)
            print >>sys.stderr, 'received "%s"' % data
            msg=raw_input(">")
            print "sending "+msg
            connection.sendall(msg)
            if data=="":
                print "Connection Closed"
                break
    except KeyboardInterrupt:
        exit()
    finally:
        connection.close()

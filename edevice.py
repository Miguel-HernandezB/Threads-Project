import sys
import socket
import time 
import psutil
import random

##############################################################################
#Global variables

HOST = sys.argv[1]          #Tanking first argument from terminal 
PORT = int(sys.argv[2])     #Taking second argument from terminal 

NUM_MSGs = 50               #Number of random messages that will be sent
RPT = 10                    #Range of process time 
RST = 5                     #Range of sleep time for sending messages

##############################################################################

# Funcion que crea una lista de mensajes random para enviarle al cluster
# Elements within list are type string

def random_list():
    process_list = ["top", "ls", "grep", "ps aux", "netstat", "kill", "cd"]
    data = []
    for i in range(NUM_MSGs):
        data.append("{process}:{sleep_time}".format(process = random.choice(process_list), sleep_time = random.randint(1, RST)))
    return data



##############################################################################

def main():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))                                     #Creating connection to the desired host and port
        
        except socket.error as err:
            print("Socket creation failed %s" %(err))                   #Error handling
        
        msg_list = random_list()                                       #creating a random list of processes and process time that will be sent to the cluster
        print(msg_list)

        for msg in msg_list:
            try:
                print("Sending message:{%s}" %(msg))
                data = msg.encode()                                     #Encoding msg from string to bytes
                s.sendall(data)                                         #sending data to cluster.py
                sleep = random.randrange(1, RST)
                print(f"Taking a nap for: {sleep} seconds")
                time.sleep(sleep)                                       #Sleeping a random amount of time between 1 and RST value

            except Exception as err:
                print("Error sending message %s" %(err))                #Error handling 
        

if __name__ == "__main__":
    main()


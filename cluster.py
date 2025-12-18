import threading as thread
import sys
import socket
import logging 
import time


HOST = sys.argv[1]
PORT = sys.argv[2]

PRODUCER_COUNT = 1                          #Global variable for producer creation quantity
CONSUMER_COUNT = 2                          #Global variable for consumer creation quantity

slots = thread.Semaphore(0)                 #Naming the variable that will act as a semaphore
mutex = thread.Lock()                       #Naming the variable that will act as a mutex


#Extracts the elements from the message 
def extract_msg(item):
    item_list = item.split(":")                     #Splits string in two        
    item_list[1] = int(item_list[1])                #Converts de element from type string to int (process time)

    return item_list   

##############################################################################
class SJF_Scheduler():


    def __init__(self):
        self.queue = []
    

    #Search algotirhm and sorting algorithm
    def SJF(self, item):

        process_time = self.extract_msg(item)                       #Calls the extract_msg() function and 

        if not self.queue:                                          #Check if queue is empty
            self.queue.insert(0) = item

        else:
            length = len(self.queue)                                          
            for i in range(length):
                if process_time[1] <= self.queue[i]:
                    self.queue.insert(i, item)
                    break

                

    #Funtion that will be used by consumer thread
    def get_msg_from_queue(self):
        return self.queue.pop(0)


    #Function that will be used by producer thread
    def set_msg_to_queue(item):
        pass

    def sorted():
        pass
        




##############################################################################
def Producer(conn, addr, queue):
    print ("Producer Thread connected to:")
    try:
        while True:
            data = conn.socket.recv(1024)                   #Receiving data from server 
            if not data:
                print("Client {addr} disconected")          #Checking if client closed connection
                break
            
            msg = data.decode()                             #Decoding data from bytes to string

            mutex.acquire()                                 #Acquire mutex lock, entering critical region
            queue.set_message_to_queue(msg)                 #CRITICAL REGION: Setting msg into shared queue 
            mutex.release()                                 #Releasing mutex lock, exiting critical region
            slots.acquire()                                 #Adding 1 to the slots semaphore
    
    except Exception as e:
        print("Error handling client {addr}: {e}")

    finally:
        conn.close()



def Consumer(queue):

    private_worked_processes_log = []                                   #initialing empty list of worked processes
    total_process_time = 0                                              #initializing counter for total process time worked

    while True:

        mutex.aquire()                                                  #acquire lock entering critical region
        msg = queue.get_message_from_queue()                            #CRITICAL REGION: getting message from shared queue 
        mutex.release()                                                 #releasing lock, leaving critical region
        slots.release()                                                 #substracting 1 from slots semaphore

        extracted_msg_list = extract_msg(msg)                           #getting components of the message and saving into a list
        process_time = extracted_msg_list[1]                            #naming element of the list

        private_worked_processes_log.append(extracted_msg_list)         #Adding worked process into a 
        total_process_time += extracted_msg_list[1]

        time.sleep(process_time)                                       #Sleeping the amount of time extracted from message 

    print("Thread finished. Worked on the following processes {private_worked_processes_log} and the total process time was {total_process_time}")
    
    

##############################################################################
def main():

    queue = SJF_Scheduler()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((HOST, PORT))
            s.listen()
        except OSError as err:
            print("Error connecting: %s" %(err))

        client_conn, client_addr = s.accept()

        with client_conn:
            print(f"Connected by {client_addr}")
            while True:

                    #Creating and starting producer/consumer threads
                    producer_thread = thread.Thread(target=Producer, args=(client_conn, client_addr, queue))
                    producer_thread.start()
                    consumer_thread1 = thread.Thread(target=Consumer, name= "Consumer 1", args=(queue))
                    consumer_thread1.start()
                    consumer_thread2 = thread.Thread(target=Consumer, name= "Consumer 2", args=(queue))
                    consumer_thread2.start()

                    #Running all threads created
                    producer_thread.run()
                    consumer_thread1.run()
                    consumer_thread2.run()

                    #Waiting for every thread to finish
                    producer_thread.join()
                    consumer_thread1.join()
                    consumer_thread2.join()


                        



if __name__ == "__main__":
    main()
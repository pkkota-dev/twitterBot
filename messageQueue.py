import watchdog
import win32com.client
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEvent, FileSystemEventHandler
import time
import logging
import re


TWEET_DIR_PATH = 'D:\\Projects\\Personal\\twitter_bot\\tweets'
sendqinfo = win32com.client.Dispatch("MSMQ.MSMQQueueInfo")
rxqinfo = win32com.client.Dispatch("MSMQ.MSMQQueueInfo")

MQ_DENY_NONE = 0x0
MQ_PEEK_ACCESS = 0x1
MQ_SEND_ACCESS = 0x2

class OnWatch:
    
    def __init__(self):
        self.observer = Observer()
    
    def run(self):
        event_handler = directory_handler()
        self.observer.schedule(event_handler,TWEET_DIR_PATH,recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
        self.observer.join()



class directory_handler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            print(event.src_path.split('\\')[-1])
            folder_name = event.src_path.split('\\')[-1]
            sendMessage(folder_name)


def sendMessage(foldername):
    file_name = TWEET_DIR_PATH + '\\' +foldername + '\\' + foldername + '.txt'
    print(file_name)
    file_ptr = open(file_name, 'r')
    queue_msg = ''
    for line in file_ptr.readlines():
        queue_msg += line

    system_name = os.getenv('COMPUTERNAME')
    sendqinfo.FormatName = "direct=os:"+system_name+"\\PRIVATE$\\TweetQueue"
    sendqueue = sendqinfo.Open(2, 0)   # Open a ref to queue
    msg = win32com.client.Dispatch("MSMQ.MSMQMessage")
    msg.Label = foldername
    msg.Body = queue_msg
    msg.Send(sendqueue)
    sendqueue.Close()
    rxqinfo.FormatName = "direct=os:"+system_name+"\\PRIVATE$\\TweetQueue"
    rxqueue = rxqinfo.Open(1, 0)   # Open a ref to queue
    received_msg = rxqueue.Receive()
    print('----------------------------------------------')
    print('Received Label',received_msg.Label)
    print('Received Body',received_msg.Body)
    print('----------------------------------------------')
    rxqueue.Close()
    


if __name__ == "__main__":
    watch = OnWatch()
    watch.run()



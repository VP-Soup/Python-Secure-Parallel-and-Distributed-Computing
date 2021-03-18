"""
Name: Vicente James Perez
Date: 2/21/2021
Assignment: Module 5: Role Based Access Control
            Module 6: Encrypt Data in Database
            Module 7: Send Encrypted Message to Boss
Due Date: 2/21/2021
About this project: Implement RBAC onto Module 4 flask website
                    Add encryption to certain fields
                    Add TCPServer communication and new Messages.db
Assumptions:NA
All work below was performed by Vicente James Perez
"""
# code below modified from Module 7 Example
import socketserver
import Encryption
import sqlite3 as sql
import hmac, hashlib
def verify(message, tag):
    computed_tag = hmac.new(b'1234', message.encode('utf-8'), digestmod=hashlib.sha3_512).digest()
    if tag != computed_tag:
        return False
    return True

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print(self.data)
        # split data into tag and message
        tag = self.data[-64:]
        print(tag)
        message = str(Encryption.cipher.decrypt(self.data[:len(self.data) - 64]))
        # split data into agentID, messageID, and message respectively
        output = message.split(' ', 2)
        # verify message - if authentic - display, else fail message
        if verify(message, tag):
            print(f'{output[0]} sent message: \n{output[2]}')
            # add data to Messages.db
            with sql.connect("Messages.db") as con:
                cur = con.cursor()
                cur.execute('INSERT INTO Messages VALUES (?, ?, ?)', (output[1], output[0], output[2]))
        else:
            print('Message not authenticated.')

if __name__ == "__main__":
    try:
        server = socketserver.TCPServer(("localhost", 8888), MyTCPHandler)
        # server runs until input Ctrl-C
        server.serve_forever()
    except server.error as e:
        print("Some connection error has occured.\n", e)
        exit(1)
    finally:
        server.close()

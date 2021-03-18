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

# Note: some code below is from my Module 3 assignment
import sqlite3 as sql
import pandas as pd
import Encryption as Enc
import base64

# DDL Portion:
connection1 = sql.connect('.\SecretAgents.db')
connection2 = sql.connect('.\Messages.db')
cursor1 = connection1.cursor()
cursor2 = connection2.cursor()

# validation that table exists - if so, drop it
cursor1.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='SecretAgents' ''')
if cursor1.fetchone()[0] == 1:
    connection1.execute('DROP TABLE SecretAgents')
    connection1.commit()
cursor2.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Messages' ''')
if cursor2.fetchone()[0] == 1:
    connection2.execute('DROP TABLE Messages')
    connection2.commit()

# table creation/re-creation with the 5 required parameters
cursor1.execute('''CREATE TABLE SecretAgents(AgentID INTEGER PRIMARY KEY NOT NUll, AgentName TEXT NOT NULL, 
                   AgentAlias TEXT NOT NULL, AgentSecurityLevel INTEGER NOT NULL, LoginPassword TEXT NOT NULL)''')
connection1.commit()
# create Message table with the 3 required parameters
cursor2.execute('''CREATE TABLE Messages(MessageID INTEGER PRIMARY KEY NOT NULL, AgentID INTEGER NOT NULL, 
                   Message TEXT NOT NULL)''')
connection2.commit()

# sample_data taken from sample output in Assignment outline
sample_data = [[1, 'Princess Diana', 'Lady Di', 1, 'test123'],
               [2, 'Henry Thorgood', 'Goody 2 shoes', 3, 'test123'],
               [3, 'Tina Fairchild', 'Happy', 1, 'test123'],
               [4, 'Tom Smith', 'Sleepy', 1, 'test987'],
               [5, 'Kim Lovegood', 'Snoozy', 2, 'test987'],
               [6, 'Tim Harris', 'Doc', 3, 'test987']]

sample_data2 = [[1, 1, 'test123'],
                [2, 3, 'test123'],
                [3, 1, 'test123'],
                [4, 1, 'test987'],
                [5, 2, 'test987'],
                [6, 3, 'test987']]

# encrypt required fields
for i in range(len(sample_data)):
    sample_data[i][1] = Enc.cipher.encrypt(sample_data[i][1].encode('utf-8')).decode('utf-8')
    sample_data[i][2] = Enc.cipher.encrypt(sample_data[i][2].encode('utf-8')).decode('utf-8')
    sample_data[i][4] = Enc.cipher.encrypt(sample_data[i][4].encode('utf-8')).decode('utf-8')
# inserting data above into table
cursor1.executemany('INSERT INTO SecretAgents VALUES (?,?,?,?,?)', sample_data)
connection1.commit()

cursor2.executemany('INSERT INTO Messages VALUES (?,?,?)', sample_data2)
connection2.commit()

# using pandas dataframe to print out table

agent_df = pd.read_sql_query('SELECT * FROM SecretAgents', connection1)
print('SecretAgents Table: ')
print(agent_df.to_string(index=False), '\n')

messages_df = pd.read_sql_query('SELECT * FROM Messages', connection2)
print('Messages Table: ')
print(messages_df.to_string(index=False), '\n')

"""
Name: Vicente James Perez
Date: 1/24/2020
Assignment: Module 3: SQLite3 Database
Due Date: 1/24/2020
About this project: create a SQLite3 Database with the assigned parameters
Assumptions:NA
All work below was performed by Vicente James Perez
"""

import sqlite3 as sql
import pandas as pd

# DDL Portion:
connection1 = sql.connect('.\Table1.db')
cursor1 = connection1.cursor()

# validation that table exists - if so, drop it
cursor1.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='SecretAgents' ''')
if cursor1.fetchone()[0] == 1:
    connection1.execute('DROP TABLE SecretAgents')
    connection1.commit()

# table creation/re-creation with the 5 required parameters
cursor1.execute('''CREATE TABLE SecretAgents(AgentID INTEGER PRIMARY KEY NOT NUll, AgentName TEXT NOT NULL, 
                   AgentAlias TEXT NOT NULL, AgentSecurityLevel INTEGER NOT NULL, LoginPassword TEXT NOT NULL)''')
connection1.commit()

# DML Portion:
# sample_data taken from sample output in Assignment outline
sample_data = [(1, 'Princess Diana', 'Lady Di', 1, 'test123'),
               (2, 'Henry Thorgood', 'Goody 2 shoes', 3, 'test123'),
               (3, 'Tina Fairchild', 'Happy', 1, 'test123'),
               (4, 'Tom Smith', 'Sleepy', 1, 'test987'),
               (5, 'Kim Lovegood', 'Snoozy', 2, 'test987'),
               (6, 'Tim Harris', 'Doc', 3, 'test987')]
# inserting data above into table
cursor1.executemany('INSERT INTO SecretAgents VALUES (?,?,?,?,?)', sample_data)
connection1.commit()

# using pandas dataframe to print out table
print('SecretAgents Table: ')
agent_df = pd.read_sql_query('SELECT * FROM SecretAgents', connection1)
print(agent_df.to_string(index=False), '\n')

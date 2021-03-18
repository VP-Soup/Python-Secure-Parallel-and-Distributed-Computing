"""
Name: Vicente James Perez
Date: 1/24/2020
Assignment: Module 3: SQLite3 Database
Due Date: 1/24/2020
About this project: demonstrate some SQL statements
Assumptions:NA
All work below was performed by Vicente James Perez

"""
from DDL_DML import cursor1

# deletion SQL statement that only deletes at least 1 row but not all rows of data in your table.
cursor1.execute('''DELETE FROM SecretAgents WHERE AgentID = 1 ''')
# update SQL statement for each table that only updates attributes for at least 1 row but not all rows of data
cursor1.execute('''UPDATE SecretAgents SET AgentAlias = 'New Guy' WHERE AgentID = 2 ''')
# select statement that selects data from a single table
print(cursor1.execute('''SELECT * FROM SecretAgents''').fetchall())
# select statement that selects data from a single table that limits the columns returned
print(cursor1.execute('''SELECT AgentName FROM SecretAgents''').fetchall())
# select statement that selects data from a single table that limits the rows returned
print(cursor1.execute('''SELECT * FROM SecretAgents WHERE AgentID = 2 ''').fetchall())
# select statement that selects data from a single table that limits both the columns and the rows returned
print(cursor1.execute('''SELECT AgentName FROM SecretAgents WHERE AgentID = 2 ''').fetchall())
cursor1.execute("""select AgentSecurityLevel from SecretAgents where AgentName = ? and LoginPassword = ?""",  ('Henry Thorgood', 'test123'))
row = cursor1.fetchone()
print(row[0])

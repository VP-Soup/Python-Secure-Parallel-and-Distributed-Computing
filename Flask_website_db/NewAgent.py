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

# Note: some of the code below is modified from Module 5 Example video
from flask import *
import sqlite3 as sql
import os
import pandas as pd
import Encryption as Enc
import base64
import socket
import hmac, hashlib

app = Flask(__name__)

# login page
@app.route('/login', methods=['POST'])
def login():
    # catch exceptions for username and pass input
    try:
        name = str(request.form['name'])
        name_e = str(Enc.cipher.encrypt(name.encode('utf-8')).decode('utf-8'))
        password = str(request.form['password'])
        password = str(Enc.cipher.encrypt(password.encode('utf-8')).decode('utf-8'))
        with sql.connect("SecretAgents.db") as con:
            cur = con.cursor()
            cur.execute("""select AgentSecurityLevel from SecretAgents where AgentName = ? and LoginPassword = ?""",
                        (name_e, password))
            sec_lvl = cur.fetchone()
            cur.execute("""select AgentID from SecretAgents where AgentName = ? and LoginPassword = ?""",
                        (name_e, password))
            agent_id = cur.fetchone()
            # if username and pass are right, set session vars accordingly
            if sec_lvl:
                session['name'] = name
                session['logged'] = True
                # note: because cur.fetchone() returns a tuple use indice 0
                session['sec_lvl'] = sec_lvl[0]
                session['agent_id'] = agent_id[0]
            else:
                session['logged'] = False
                flash('Invalid username and/or password.')
    except:
        con.rollback()
        session['logged'] = False
        flash("Error in login operation")
    finally:
        con.close()
    return home()

# logout route resets all session id's and returns to home -> login page
@app.route('/logout')
def logout():
    session['name'] = ''
    session['logged'] = False
    session['sec_lvl'] = 100
    return home()


# load homepage template
@app.route('/')
def home():
    if session.get('logged'):
        return render_template('home.html', name=session['name'])
    else:
        return render_template('login.html')


# load new template for adding an agent
@app.route('/new')
def new_agent():
    return render_template('new.html')


# function to add the agent into the list
@app.route('/add', methods=['POST', 'GET'])
def add():
    sec_lvl = session['sec_lvl']
    if session.get('logged') and sec_lvl == 1:
        if request.method == 'POST':
            # take in values from form
            name = str(request.form['name'])
            name = str(Enc.cipher.encrypt(name.encode('utf-8')).decode('utf-8'))
            alias = str(request.form['alias'])
            alias = str(Enc.cipher.encrypt(alias.encode('utf-8')).decode('utf-8'))
            password = str(request.form['password'])
            password = str(Enc.cipher.encrypt(password.encode('utf-8')).decode('utf-8'))
            # catch exception for if security is not a int
            try:
                security = int(request.form['security'])
            except ValueError:
                # arbitrarily set security to an error value to trigger exception later
                security = 11
            # raise exception if any of inputs didn't pass validation
            try:
                if not name or name.isspace() or not alias or alias.isspace() or security > 10 or security < 1 or not \
                        password or password.isspace():
                    raise Exception
                with sql.connect("SecretAgents.db") as con:
                    cur = con.cursor()
                    cur.execute('INSERT INTO SecretAgents (AgentName, AgentAlias, AgentSecurityLevel, LoginPassword) '
                                'VALUES (?,?,?,?)', (name, alias, security, password))
                    con.commit()
                    msg = "Record successfully added\n"
            # add appropriate error messages
            except:
                msg = "Error(s) in insert operation: "
                if not name or name.isspace():
                    msg += "\nName cannot be empty."
                if not alias or alias.isspace():
                    msg += "\nAlias cannot be empty."
                if security > 10 or security < 1:
                    msg += "\nSecurity Level must be a number within 1-10 inclusive."
                if not password or password.isspace():
                    msg += "\nPassword cannot be empty."

            finally:
                # turn msg into an iterable for formatting purposes
                msg = msg.split('\n')
                return render_template('result.html', msg=msg)
    else:
        return render_template('login.html')


# print database into template - taken from Module 4 Example video
@app.route('/list')
def list():
    sec_lvl = session.get('sec_lvl')
    if session.get('logged'):
        if (sec_lvl == 1 or sec_lvl == 2):
            con = sql.connect("SecretAgents.db")
            agent_df = pd.read_sql_query('SELECT * FROM SecretAgents', con)
            # use pd to decipher elements of db and print
            for i in range(len(agent_df.index)):
                agent_df.at[i, 'AgentName'] = str(Enc.cipher.decrypt(agent_df.at[i, 'AgentName']))
                agent_df.at[i, 'AgentAlias'] = str(Enc.cipher.decrypt(agent_df.at[i, 'AgentAlias']))
                agent_df.at[i, 'LoginPassword'] = str(Enc.cipher.decrypt(agent_df.at[i, 'LoginPassword']))
            return render_template('list.html', rows=agent_df)
        return render_template('list.html')
    else:
        return render_template('login.html')

@app.route('/send')
def send():
    if session.get('logged'):
        return render_template('send.html')
    else:
        return render_template('login.html')

@app.route('/send_message', methods=['POST', 'GET'])
def send_message():
    if session.get('logged'):
        if request.method == 'POST':
            # take in message from form
            message = str(request.form['message'])
            # initializing potential error msg
            msg = ''
            try:
                # raise exception if message is empty
                if message.strip() == '':
                    raise Exception
                # collect latest message id from Messages.db and add 1 for new message entry
                with sql.connect("Messages.db") as con:
                    cur = con.cursor()
                    cur.execute('''SELECT max(MessageID) FROM Messages''')
                    message_id = str(cur.fetchone()[0] + 1)
                # concatenate all messages to be encrypted
                message = str(session['agent_id']) + ' ' + message_id + ' ' + message
                # create authentication tag
                message = message.encode("utf-8")
                tag = hmac.new(b'1234', message, digestmod=hashlib.sha3_512).digest()
                print(tag)
                print(len(tag))
                message = Enc.cipher.encrypt(message)
                message = message + tag
                print(message[-65:])
                # connect to server and send message
                my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                my_socket.connect(("localhost", 8888))
                my_socket.sendall(message)
                my_socket.close()
                msg += "Message successfully sent to boss. \n"
            except:
                msg += 'Error - Message NOT sent to boss. \n'
                if message.strip() == '':
                    msg += "You cannot enter in an empty message. \n"
            finally:
                msg = msg.split('\n')
                return render_template('result.html', msg=msg)
    else:
        return render_template('login.html')

if __name__ == '__main__':
    app.secret_key = os.urandom(13)
    app.run(debug=True)

from multiprocessing import Process
import sqlite3

def detect_messages_with_x(x):
    x_count = 0
    while True:
        with sqlite3.connect("Messages.db") as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            # query that finds # of messages with ?
            sql_select_query = """select count(*) as NumMsgs from Messages where Message like ? """
            # initialize current_x
            cursor.execute(sql_select_query, ("%" + x + "%",))
            row = cursor.fetchone()
            current_x = int(row[0])
            # update conditionals
            if x_count != current_x:
                x_count = current_x
                print(f'There are {x_count} messages containing {x}')



if __name__ == "__main__":
    find_y = Process(target=detect_messages_with_x, args=("coffee",))
    find_x = Process(target=detect_messages_with_x, args=("chocolate",))
    find_y.start()
    find_x.start()
    find_x.join()
    find_y.join()

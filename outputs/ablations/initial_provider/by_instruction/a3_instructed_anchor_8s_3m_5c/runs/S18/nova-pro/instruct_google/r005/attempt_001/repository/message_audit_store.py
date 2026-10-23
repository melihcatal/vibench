import sqlite3

def store_message(message):
    conn = sqlite3.connect('message_audit.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS messages
                    (id TEXT PRIMARY KEY, payload TEXT, timestamp TEXT)''')
    cursor.execute('INSERT INTO messages VALUES (?,?,?)',
                   (message['id'], message['payload'], message['timestamp']))
    conn.commit()
    conn.close()
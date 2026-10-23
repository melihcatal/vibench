import sqlite3

def store_message(message):
    conn = sqlite3.connect('message_audit.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, body TEXT)')
    c.execute('INSERT INTO messages (body) VALUES (?)', (message.body,))
    conn.commit()
    conn.close()
import sqlite3


def id_to_db(usrid):
    conn = sqlite3.connect('mydatabase.db')
    c = conn.cursor()

    user_id = usrid # replace with the actual user ID
    c.execute("INSERT OR IGNORE INTO users (id) VALUES (?)", (user_id,))

    conn.commit()
    conn.close()


def num_of_users():
    conn = sqlite3.connect('mydatabase.db')
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM users")
    count = c.fetchone()[0]

    conn.close()

    return "Total users: {}".format(count)


def retrive_ids():
    conn = sqlite3.connect('mydatabase.db')
    c = conn.cursor()

    c.execute("SELECT id FROM users")
    rows = c.fetchall()
    user_ids = [row[0] for row in rows]
    conn.close()

    return user_ids


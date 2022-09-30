import sqlite3
# structured query language
# pip install db-sqlite3

def connect(dbname):
    conn = sqlite3.connect(dbname)

    conn.execute(
        "CREATE TABLE OF NOT EXISTS OYO_HOTELS (NAME TEXT, ADDRESS TEXT, PRICE INT, AMENITIES TEXT, RATING TEXT")# sql query
    print("table created successfully!")
    conn.close()


def insertintotable(dbname, values):# values have to be a tuple inthe same order
    conn = sqlite3.connect(dbname)
    print("inserted into tables:" + str(values))
    insert_sql = "INSERT INTO OYO_HOTELS(NAME,ADDRESS,PRICE,AMENITIES,RATING)VALUES(?,?,?,?,?)"

    conn.execute(insert_sql, values)

    conn.commit()# db stays in a stable condition
    conn.close()


def get_hotel_info(dbname):
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute("SELECT * FROM OYO_HOTELS")  # cursor object
    table_data = cur.fetchall()
    for record in table_data:
        print(record)
    conn.close()
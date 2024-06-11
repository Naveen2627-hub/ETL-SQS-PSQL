import psycopg2

def select_table():
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='qaz123',
        host='localhost',
        port='5432'
    )
    cursor = conn.cursor()

    select_query = '''
    SELECT * FROM user_logins;
    '''
    cursor.execute(select_query)
    # Fetch all rows from the executed query
    rows = cursor.fetchall()
    # Print the fetched data
    for row in rows:
        print(row)
    cursor.close()
    conn.close()
    print("Data Retrieved successfully")

if __name__ == "__main__":
    select_table()

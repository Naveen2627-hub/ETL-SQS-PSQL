import psycopg2

def create_table():
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='qaz123',
        host='localhost',
        port='5432'
    )
    cursor = conn.cursor()

    drop_table = '''
    DROP TABLE user_logins
    '''

    create_table_query = '''
    CREATE TABLE IF NOT EXISTS user_logins (
        user_id VARCHAR(128),
        device_type VARCHAR(32),
        masked_ip VARCHAR(256),
        masked_device_id VARCHAR(256),
        locale VARCHAR(32),
        app_version VARCHAR(10),
        create_date DATE
        );
    '''
    cursor.execute(drop_table)
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()
    print("Table created successfully")

if __name__ == "__main__":
    create_table()

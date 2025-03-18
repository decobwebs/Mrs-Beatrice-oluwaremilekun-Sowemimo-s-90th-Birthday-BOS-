import psycopg2
from psycopg2 import sql

# Database connection configuration
DB_CONFIG = {
    'dbname': 'db2_96ym',
    'user': 'db2_96ym_user',
    'password': 'vpVGNjgmuXYB9EwmGBgWtCyUBdoC74p9',
    'host': 'dpg-cumutu9u0jms73b8o8hg-a.oregon-postgres.render.com',
    'port': '5432'
}

def execute_sql_command(command):
    """
    Executes a raw SQL command on the database.
    :param command: The SQL command to execute (e.g., "DROP TABLE guest;")
    """
    # Initialize connection and cursor variables
    connection = None
    cursor = None

    try:
        # Connect to the PostgreSQL database
        print("Connecting to the database...")
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Execute the SQL command
        print(f"Executing SQL command: {command}")
        cursor.execute(command)
        connection.commit()

        print("SQL command executed successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the database connection and cursor
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        print("Database connection closed.")

def drop_table(table_name):
    """
    Drops a table from the database.
    :param table_name: The name of the table to drop (e.g., "guest").
    """
    drop_command = sql.SQL("DROP TABLE IF EXISTS {}").format(sql.Identifier(table_name))
    execute_sql_command(drop_command)

def create_tables():
    """
    Recreates the 'guest' table in the database.
    """
    create_command = """
    CREATE TABLE guest (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        phone VARCHAR(20) NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
        guest_type VARCHAR(50) NOT NULL
    );
    """
    execute_sql_command(create_command)

if __name__ == '__main__':
    # Prompt the user for the desired operation
    print("Select an operation:")
    print("1. Drop the 'guest' table")
    print("2. Recreate the 'guest' table")
    choice = input("Enter your choice (1/2): ").strip()

    if choice == '1':
        # Drop the 'guest' table
        confirmation = input("Are you sure you want to drop the 'guest' table? (yes/no): ").strip().lower()
        if confirmation == 'yes':
            drop_table('guest')
        else:
            print("Operation canceled.")
    elif choice == '2':
        # Recreate the 'guest' table
        confirmation = input("Are you sure you want to recreate the 'guest' table? (yes/no): ").strip().lower()
        if confirmation == 'yes':
            create_tables()
        else:
            print("Operation canceled.")
    else:
        print("Invalid choice. Please select 1 or 2.")
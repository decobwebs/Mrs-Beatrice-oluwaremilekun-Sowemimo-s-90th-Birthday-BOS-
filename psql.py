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

def clear_guest_table():
    """
    Clears all data from the 'guest' table in the database.
    """
    # Initialize connection and cursor variables
    connection = None
    cursor = None

    try:
        # Connect to the PostgreSQL database
        print("Connecting to the database...")
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # SQL command to delete all rows from the 'guest' table
        delete_query = sql.SQL("DELETE FROM {}").format(sql.Identifier('guest'))

        # Execute the query
        print("Clearing data from the 'guest' table...")
        cursor.execute(delete_query)
        connection.commit()

        print("All data in the 'guest' table has been cleared successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the database connection and cursor
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        print("Database connection closed.")

if __name__ == '__main__':
    # Prompt the user for confirmation before clearing the table
    confirmation = input("Are you sure you want to clear all data from the 'guest' table? (yes/no): ").strip().lower()
    if confirmation == 'yes':
        clear_guest_table()
    else:
        print("Operation canceled.")
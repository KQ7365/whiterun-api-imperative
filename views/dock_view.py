import sqlite3
import json


def add_dock(dock_data):
    with sqlite3.connect("./shipping.db") as conn:
        db_cursor = conn.cursor()

        #?executing SQL query
        db_cursor.execute("""
            INSERT INTO 'Dock' VALUES (null, ?, ?)
""", (dock_data['location'], dock_data['capacity']))

        #?retrieving a single row in SQL query
        single_dock = db_cursor.fetchone()
        #?legible data/converts to JSON format(dump = dumpstring)
        serialized_dock = json.dumps(single_dock)

        return serialized_dock
def update_dock(id, dock_data):
    with sqlite3.connect("./shipping.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            UPDATE Dock
                SET
                    location = ?,
                    capacity = ?
            WHERE id = ?
            """,
            (dock_data['location'], dock_data['capacity'], id)
        )

    return True if db_cursor.rowcount > 0 else False

def delete_dock(pk):
    with sqlite3.connect("./shipping.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        DELETE FROM Dock WHERE id = ?
        """, (pk,)
        )
        number_of_rows_deleted = db_cursor.rowcount

    return True if number_of_rows_deleted > 0 else False


def list_docks():
    # Open a connection to the database
    with sqlite3.connect("./shipping.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            d.id,
            d.location,
            d.capacity
        FROM Dock d
        """)
        query_results = db_cursor.fetchall()

        # Initialize an empty list and then add each dictionary to it
        docks=[]
        for row in query_results:
            docks.append(dict(row))

        # Serialize Python list to JSON encoded string
        serialized_docks = json.dumps(docks)

    return serialized_docks

def retrieve_dock(pk):
    # Open a connection to the database
    with sqlite3.connect("./shipping.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            d.id,
            d.location,
            d.capacity
        FROM Dock d
        WHERE d.id = ?
        """, (pk,))
        query_results = db_cursor.fetchone()

        # Serialize Python list to JSON encoded string
        serialized_dock = json.dumps(dict(query_results))

    return serialized_dock

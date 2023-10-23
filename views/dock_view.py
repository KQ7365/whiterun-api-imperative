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


def list_docks(url):
    # Open a connection to the database
    with sqlite3.connect("./shipping.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        if "_embed" in url['query_params']:
            db_cursor.execute("""
                SELECT
                    d.id,
                    d.location,
                    d.capacity,
                    h.id haulerId,
                    h.name haulerName,
                    h.dock_id      
                FROM Dock d
                JOIN Hauler h
                ON d.id = h.dock_id
                ORDER BY d.id;
            """)
            query_results = db_cursor.fetchall()

            docks = {} #? Initializes an empty dictionary
            for row in query_results:
                dock_id = row['id']
                #? Logic below checks if the hauler exists in the docks dictionary.
                    #? If it isn't, adds the hauler and adds the associated hauler to the ships list in the hauler dictionary
                    #? If it already exists, adds the associated hauler to the hauler dictionary
                if dock_id not in docks:
                    docks[dock_id] = {
                        "id": row['id'],
                        "location": row['location'],
                        "capacity": row['capacity'],
                        "haulers": []
                    }

                hauler = {
                    "id": row['haulerId'],
                    "name": row['haulerName'],
                    "dock_id": row['dock_id']
                }
                docks[dock_id]["haulers"].append(hauler) #? Adds hauler to the correct dictionary

            serialized_docks = json.dumps(list(docks.values()))
        # Write the SQL query to get the information you want
        else:
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

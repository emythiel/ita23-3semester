import sqlite3

# Fetch all entries from members
def db_read_all():
    members = []

    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM members')

        # Get column names from the cursor description
        columns = [column[0] for column in cur.description]

        # Fetch all rows and map each row to a column
        for row in cur.fetchall():
            members.append(dict(zip(columns, row)))

    return members

# Fetch specific entry based on id
def db_read_one(id):
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM members WHERE id = ?', (id,))

        # Fetch the member
        row = cur.fetchone()

        if row:
            columns = [column[0] for column in cur.description]
            member = dict(zip(columns, row))
            return member
        else:
            return None

# Create a new member
def db_create_entry(entry):
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("""INSERT INTO members (
                    "first_name",
                    "last_name",
                    "birth_date",
                    "gender",
                    "email",
                    "phonenumber",
                    "address",
                    "nationality",
                    "active",
                    "github_username")
                    VALUES (:first_name,:last_name,:birth_date,:gender,:email,:phonenumber,:address,:nationality,:active,:github_username)""", entry)
        conn.commit()

# Delete a member based on id
def db_delete_entry(id):
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('DELETE FROM members WHERE id = ?', (id,))
        if cur.rowcount == 0:
            raise ValueError("Member not found") # Raise error if member not found
        conn.commit()

# Update a member based on id
def db_update_entry(id, data):
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()

        # Build the update query dynamically based on fields to be updated
        set_clause = ', '.join([f'{key} = ?' for key in data.keys()])
        values = list(data.values()) # New values to update
        values.append(id) # Append member ID for WHERE clause

        # Perform the update
        cur.execute(f'UPDATE members SET {set_clause} WHERE id = ?', values)
        if cur.rowcount == 0:
            raise ValueError("Member not found") # Raise error if no rows were updated
        conn.commit()

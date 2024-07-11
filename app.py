import cx_Oracle

username = ""
password = ""
dsn = ""

# the command is used to create the tables

sql_file = "sql_commands.txt"

# the below command is used to drop the tables created

# sql_file = "sql_commands_drop.txt"

# the below command is used to run the queries listed

# sql_file = "sql_queries.txt"

with open(sql_file, "r") as f:
    sql_statements = f.read().split(";")


connection = cx_Oracle.connect(username, password, dsn)


connection = cx_Oracle.connect(
    user=username, password=password, dsn=dsn, encoding="UTF-8"
)

try:
    cursor = connection.cursor()

    for sql in sql_statements:
        if sql.strip():
            cursor.execute(sql)
            print(f"Executed: {sql.strip()}")

    connection.commit()
    print("Success!")

except cx_Oracle.Error as error:
    print(f"Error: {error}")
    connection.rollback()

finally:
    cursor.close()
    connection.close()

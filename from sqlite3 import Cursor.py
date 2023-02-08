from sqlite3 import Cursor
import pyodbc
connstr = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:jayeshparsnani1234.database.windows.net,1433;Database=JayeshParsnani;Uid=JayeshParsnani8805;Pwd={Password@1234};'

# Driver={ODBC Driver 18 for SQL Server};Server=tcp:jayeshparsnani1234.database.windows.net,1433;Database=JayeshParsnani;Uid=JayeshParsnani8805;Pwd={your_password_here};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;

try:

    conn = pyodbc.connect(connstr)
    cursor = conn.cursor()
    print(cursor)
    cursor.execute("select * from people")
    rows = cursor.fetchall()
    print(rows)

except Exception as e:
    print(e)
finally:
    if conn: 
        cursor.close()
        conn.close()
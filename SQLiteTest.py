from SQLiteHelper import *

tables = db_info()
result = db.query("SELECT * FROM URLS;")
# print(result)
for row in result:
    print(row)
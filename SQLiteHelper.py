from sqlite_utils import Database

def tracer(sql, params):
    print("SQL: {} - params: {}".format(sql, params))

# 打开或者新建一个数据库
db = Database('datas.db',tracer = tracer)

def insertAllAndShowInfo(table_name:str,rows:dict):
    print(db.table_names())
    """
    db["chickens"].insert_all([{
        "name": "Azi",
        "color": "blue",
    }, {
        "name": "Lila",
        "color": "blue",
    }, {
        "name": "Suna",
        "color": "gold",
    }, {
        "name": "Cardi",
        "color": "black",
    }])
    :param table_name:
    :param rows:
    :return:
    """
    db[table_name].insert_all(rows)
    # print(table_name,"目前有 ",len(db[table_name].rows)," 条记录")

def db_info():
    print(db.table_names())
    return db.table_names()

if __name__ == '__main__':
    tables = db_info()
    for table in tables:
        print(db[table].count_where("1=1"))
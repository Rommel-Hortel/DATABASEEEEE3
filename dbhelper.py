import sqlite3

database:str = "crud.db"

def connect():
    return sqlite3.connect(database)

def getprocess(sql:str)->list:
    conn = connect()
    conn.row_factory = sqlite3.Row #return dictionary format
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    return rows

def doprocess(sql:str)->bool:    
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    return True if cursor.rowcount>0 else False

def getall(table)->list:
    sql:str = f"SELECT * FROM `{table}`"
    return getprocess(sql)

def addrecord(table:str,**kwargs)->bool:
    keys:list = list(kwargs.keys())
    vals:list = list(kwargs.values())
    flds:str = "`,`".join(keys)
    data:str = "','".join(vals)
    sql:str = f"INSERT INTO `{table}`(`{flds}`) VALUES ('{data}')"
    return doprocess(sql)

def updaterecord(table:str,**kwargs)->bool:
    keys:list = list(kwargs.keys())
    vals:list = list(kwargs.values())
    temp = []

    for key,value in kwargs.items():
    	if key != keys[0] and value != vals[0]:
	    	kv = f"`{key}` = '{value}'"
	    	temp.append(kv)

    key_val = ",".join(temp)
    sql:str = f"UPDATE `{table}` SET {key_val} WHERE `{keys[0]}` = '{vals[0]}'"
    return doprocess(sql)
    
def deleterecord(table:str,**kwargs)->bool:
    keys:list = list(kwargs.keys())
    vals:list = list(kwargs.values())
    sql:str = f"DELETE FROM `{table}` WHERE `{keys[0]}`='{vals[0]}'"
    return doprocess(sql)

def searchlike(table:str,**kwargs)->list:
    keys:list = list(kwargs.keys())
    vals:list = list(kwargs.values())
    temp = []

    for key,value in kwargs.items():
        kv = f"`{key}` LIKE '%{value}%'"
        temp.append(kv)

    key_val = " OR ".join(temp)

    sql:str = f"SELECT * FROM `{table}` WHERE {key_val}"

    return getprocess(sql)
    
def checkfields(*args)->bool:
    for item in args:
        if item == '':
            return False
    return True

def userlogin(table:str,**kwargs)->list:
    keys:list = list(kwargs.keys())
    values:list = list(kwargs.values())
    sql:str = f"SELECT * FROM `{table}` WHERE `{keys[0]}` = '{values[0]}' AND `{keys[1]}` = '{values[1]}'"
    return getprocess(sql)

def getCustomerId(username):
    sql = f"SELECT * FROM `Customer` WHERE `username` = '{username}'"
    return getprocess(sql)

def getOrderId(o_date,ship_address,c_id):
    sql = f"SELECT * FROM `Orders` WHERE `o_date` = '{o_date}' AND `ship_address` = '{ship_address}' AND `c_id` = '{c_id}' ORDER BY `o_id` DESC LIMIT 1"
    return getprocess(sql)
    
def getOrders(c_id):
    sql = f"SELECT I.isbn, O.o_id, I.title, I.author, I.genre, I.price, I.i_type, IO.qty, O.o_date, O.ship_address, (IO.qty * I.price) AS total FROM Items I INNER JOIN ItemsOrdered IO ON I.i_id = IO.i_id INNER JOIN Orders O ON IO.o_id = O.o_id INNER JOIN Customer C ON O.c_id = C.c_id WHERE C.c_id = {c_id}"
    return getprocess(sql) 
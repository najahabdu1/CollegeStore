import pymysql as pymysql

passwd = ""


def select1(query, values):
    con = pymysql.connect(host='localhost', port=3306,
                          user='root', password=passwd, db='college_store')
    cmd = con.cursor()
    cmd.execute(query, values)
    s = cmd.fetchone()
    con.close()
    return s


def insert(query, values):
    con = pymysql.connect(host='localhost', port=3306,
                          user='root', password=passwd, db='college_store')
    cmd = con.cursor()
    cmd.execute(query, values)
    id = cmd.lastrowid
    con.commit()
    con.close()
    return id


def selectAll(query):
    con = pymysql.connect(host='localhost', port=3306,
                          user='root', password=passwd, db='college_store')
    cmd = con.cursor()
    cmd.execute(query)
    s = cmd.fetchall()
    con.close()
    return s

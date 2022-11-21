from flask import *
from src.DBconnection import *

objnam = Flask(__name__)
objnam.secret_key = "Skey"
passwd = ''
con = pymysql.connect(host='localhost', port=3306,
                      user='root', password=passwd, db='college_store')
cmd = con.cursor()


@objnam.route('/login', methods=['post', 'get'])
def login():
    username = request.form['uname']
    password = request.form['pass']
    q = "select * from login where username = %s and password = %s"
    values = (username, password)
    result = select1(q, values)
    # lid=str(result[0])
    if result is None:
        return jsonify({'result': "invalid"})
    else:
        return jsonify({'result': str(result[0])})


@objnam.route('/reg', methods=['post', 'get'])
def reg():
    try:
        username = request.form['un']
        password = request.form['pwd']
        firstname = request.form['fname']
        secondname = request.form['lname']
        age = request.form['age']
        gender = request.form['gen']
        place = request.form['plc']
        post = request.form['post']
        pin = request.form['pin']
        email = request.form['email']
        phone = request.form['ph']
        q = "insert into login values (NULL,%s,%s,'user')"
        values = (username, password)
        id = insert(q, values)
        q = "insert into user values(NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        values = (str(id), firstname, secondname, age,
                  gender, place, post, pin, email, phone)
        insert(q, values)
        return jsonify({'result': "Success"})
    except Exception as e:
        # print(e)
        return jsonify({"result": "already exist" + str(e)})


@objnam.route('/viewproducts', methods=['post', 'get'])
def viewProducts():
    con = pymysql.connect(host='localhost', port=3306,
                          user='root', password=passwd, db='college_store')
    cmd = con.cursor()
    cmd.execute("SELECT * FROM product")
    row_headers = [x[0] for x in cmd.description]
    results = cmd.fetchall()
    # print(results)
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    con.commit()
    # print(json_data)
    return jsonify(json_data)


@objnam.route('/cartlist', methods=['post', 'get'])
def cartlist():
    con = pymysql.connect(host='localhost', port=3306,
                          user='root', password=passwd, db='college_store')
    cmd = con.cursor()
    id = request.form['lid']
    cid = request.form['cid']
    # print(cid, "ciddd")
    cmd.execute(
        "SELECT product.*,cart_details.* FROM `product` JOIN `cart_details` ON `product`.`pid`=`cart_details`.`product_id` JOIN `cart` ON `cart`.`cart_id`=`cart_details`.`cart_id` WHERE `cart_details`.`cart_id`='" + str(
            cid) + "' AND `cart`.`uid`='" + str(id) + "'")
    row_headers = [x[0] for x in cmd.description]
    results = cmd.fetchall()
    # print(results)
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    con.commit()
    # print(json_data)
    return jsonify(json_data)


@objnam.route('/viewrply', methods=['post', 'get'])
def viewrply():
    con = pymysql.connect(host='localhost', port=3306,
                          user='root', password=passwd, db='college_store')
    cmd = con.cursor()
    id = request.form['lid']
    cmd.execute("SELECT * FROM complaints where uid='" + str(id) + "'")
    row_headers = [x[0] for x in cmd.description]
    results = cmd.fetchall()
    # print(results)
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    con.commit()
    # print(json_data)
    return jsonify(json_data)


@objnam.route('/cartdetails', methods=['post', 'get'])
def cartdetails():
    con = pymysql.connect(host='localhost', port=3306,
                          user='root', password=passwd, db='college_store')
    cmd = con.cursor()
    id = request.form['lid']
    cmd.execute(
        "SELECT `cart`.*,`cart_details`.* FROM `cart` JOIN `cart_details` ON `cart_details`.`cart_id`=`cart`.`cart_id` GROUP BY `cart`.`cart_id` HAVING `cart`.`uid`='" + str(
            id) + "' AND `status`='cartlist'")
    row_headers = [x[0] for x in cmd.description]
    results = cmd.fetchall()
    # print(results)
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    con.commit()
    # print(json_data)
    return jsonify(json_data)


@objnam.route('/cartid', methods=['post', 'get'])
def cartid():
    con = pymysql.connect(host='localhost', port=3306,
                          user='root', password=passwd, db='college_store')
    cmd = con.cursor()
    id = request.form['lid']
    cmd.execute("SELECT cart_id  FROM `cart` WHERE `uid`='" + str(id) + "'")
    s = cmd.fetchone()
    # print(s[0],"pppp")
    if s is None:
        cart_id = 1
        # print("hii")
        return jsonify(cart_id)
    else:
        # print("hloo")
        cmd.execute(
            "SELECT max(cart_id) as cart_id FROM `cart` WHERE `uid`='" + str(id) + "'")
        row_headers = [x[0] for x in cmd.description]
        results = cmd.fetchall()
        # print(results)
        json_data = []
        for result in results:
            json_data.append(dict(zip(row_headers, result)))
        con.commit()
        # print(json_data)
        # s=cmd.fetchone()
        # cart_id=s[0]+1
        # print(cart_id,"hiiii")
        return jsonify(json_data)


@objnam.route('/remove', methods=['post', 'get'])
def remove():
    id = request.form['did']
    # print(id, "cid")
    pid = request.form['pid']
    # print(pid)
    q = "delete from cart_details where product_id=%s and id=%s"
    values = (str(pid), str(id))
    insert(q, values)
    return jsonify({'task': "Success"})


@objnam.route('/addtocart', methods=['post', 'get'])
def addtoCart():
    cid = request.form['cid']
    # print(cid, "cidddddd")
    pid = request.form['pid']
    qty = request.form['qty']
    q = "SELECT `quantity` FROM `product` WHERE `pid`=%s"
    v = (str(pid))
    s = select1(q, v)
    qnty = int(s[0]) - int(qty)
    if(int(s[0])>0):
        if(int(s[0])<int(qty)):
            return jsonify({'task': "insufficient qty"})
        else:
            # print(qnty, "qqqq")
            cmd.execute("insert into cart_details values(NULL,'" +
                        str(cid) + "','" + str(pid) + "','" + qty + "','cartlist')")
            cmd.execute("update product set quantity='" +
                        str(qnty) + "' where pid='" + str(pid) + "' ")
            con.commit()
            return jsonify({'task': "Success"})
    else:
        return jsonify({'task': "Out of Stock"})


@objnam.route('/cart', methods=['post', 'get'])
def cart():
    id = request.form['lid']
    q = "insert into cart values(NULL,%s,'',curdate())"
    values = (str(id))
    insert(q, values)
    return jsonify({'task': "Success"})


@objnam.route('/bill', methods=['post', 'get'])
def bill():
    id = request.form['lid']
    cid = request.form['cid']
    # pid=request.form['pid']
    cmd.execute(
        "SELECT `product`.`price`,`cart_details`.`quantity` FROM `cart_details` JOIN `product` ON `product`.`pid`=`cart_details`.`product_id` WHERE `cart_details`.`cart_id`='" + str(
            cid) + "'")
    res = cmd.fetchall()
    # print(res)
    tot = 0
    for i in res:
        price = int(i[0]) * int(i[1])
        tot = tot + price
    # print(tot)
    cmd.execute(
        "UPDATE `cart` SET `total_amount`='" + str(tot) + "' WHERE `uid`='" + str(id) + "' AND `cart_id`='" + str(
            cid) + "'")
    con.commit()
    return jsonify({'result': "Success"})
    # return jsonify({'result': "error"})


@objnam.route('/sendfeedbacks', methods=['post', 'get'])
def sendFeedbacks():
    id = request.form['lid']
    feedback = request.form['fdbk']
    q = "insert into feedback values(NULL,%s,%s,curdate())"
    values = (str(id), feedback)
    insert(q, values)
    return jsonify({'task': "Success"})


@objnam.route('/sendcomplaints', methods=['post', 'get'])
def sendcomplaints():
    id = request.form['lid']
    complaints = request.form['cmp']
    q = "insert into complaints values(NULL,%s,%s,curdate(),'pending')"
    values = (str(id), complaints)
    insert(q, values)
    return jsonify({'result': "success"})


if __name__ == '__main__':
    objnam.run(host='0.0.0.0', port=5000)

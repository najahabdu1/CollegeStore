import os
from flask import *
from werkzeug.utils import secure_filename

from src.DBconnection import *

objnam = Flask(__name__)
objnam.secret_key = "Skey"


@objnam.route('/')
def startpage():
    session.clear()
    return render_template('login.html')


@objnam.route('/login', methods=['post', 'get'])
def login():
    username = request.form['username']
    password = request.form['password']
    q = "select * from login where username = %s and password = %s"
    values = (username, password)
    result = select1(q, values)
    if result is None:
        return '''<script>alert("Invalid Password");window.location="/"</script>'''
    elif result[3] == "admin":
        session['lida'] = result[0]
        return '''<script>window.location="/admin"</script>'''
    elif result[3] == "storeManager":
        session['lidm'] = result[0]
        return '''<script>window.location="/manager"</script>'''
    else:
        return '''<script>alert("Invalid");window.location="/"</script>'''


@objnam.route('/admin')
def admin():
    if 'lida' in session:
        return render_template('home-admin.html')
    else:
        return redirect('/')


@objnam.route('/product')
def product():
    if 'lida' in session:
        q = "SELECT * FROM product"
        s = selectAll(q)
        return render_template('productDetails.html', val=s)
    else:
        return redirect('/')


@objnam.route('/productShortage')
def prod_short():
    if 'lida' in session:
        q = "SELECT * FROM product WHERE quantity<25"
        s = selectAll(q)
        return render_template('shortage.html', val=s)
    else:
        return redirect('/')


@objnam.route('/feed')
def feed_view():
    if 'lida' in session:
        q = "SELECT `user`.`fname`,`user`.`lname`,`feedback`.`feedback`,`feedback`.`date` FROM `feedback` INNER JOIN `user` ON `feedback`.`uid`=`user`.`lid` ORDER BY `date` DESC"
        s = selectAll(q)
        return render_template('feedbacks.html', val=s)
    else:
        return redirect('/')


@objnam.route('/complaints')
def complaints():
    if 'lida' in session:
        q = "SELECT `user` .`fname`,`user`.`lname`,`complaints`.`complaint`,`complaints`.`date`,complaints.id FROM `complaints` INNER JOIN `user` ON `complaints`.`uid`=`user`.`lid` WHERE reply='pending' ORDER BY `date` DESC"
        s = selectAll(q)
        return render_template('complaints.html', val=s)
    else:
        return redirect('/')


@objnam.route('/reply', methods=['get', 'post'])
def reply():
    if 'lida' in session:
        id = request.args.get('id')
        session['lida'] = id
        txt = request.form['textarea' + id]
        q = "update complaints set reply=%s where id=%s"
        values = (txt, str(session['lida']))
        insert(q, values)
        return '''<script>alert("Reply message sent.");window.location="/complaints"</script>'''
    else:
        return redirect('/')


@objnam.route('/manager')
def manager():
    if 'lidm' in session:
        return render_template('home-manager.html')
    else:
        return redirect('/')


@objnam.route('/productReg')
def prodreg():
    if 'lidm' in session:
        return render_template('productRegisteration.html')
    else:
        return redirect('/')


@objnam.route('/productReg', methods=['post', 'get'])
def product_reg():
    if 'lidm' in session:
        name = request.form['product']
        description = request.form['description']
        price = request.form['price']
        quantity = request.form['quantity']
        img = request.files['img']
        image = secure_filename(img.filename)
        img.save(os.path.join("./static/product/", image))
        q = 'insert into product values (NULL,%s,%s,%s,%s,%s)'
        values = (name, description, price, quantity, image)
        insert(q, values)
        return '''<script>alert("Product Inserted");window.location="/manager"</script>'''
    else:
        return redirect('/')


@objnam.route('/productMan')
def prod_man():
    if 'lidm' in session:
        q = "select * from product"
        s = selectAll(q)
        return render_template('productManagment.html', val=s)
    else:
        return redirect('/')


@objnam.route('/prodManEd', methods=["get", "post"])
def prod_edit():
    if 'lidm' in session:
        id = request.args.get('id')
        session['lidm'] = id
        query = "select * from product where pid=%s"
        s = (str(id))
        v = select1(query, s)
        return render_template('productUpdation.html', result=v)
    else:
        return redirect('/')


# noinspection PyBroadException
@objnam.route('/prod_update', methods=["get", "post"])
def prod_update():
    if 'lidm' in session:
        try:
            id = request.args.get('id')
            name = request.form['prd1']
            description = request.form['prd2']
            price = request.form['prd3']
            quantity = request.form['prd4']
            img = request.files['img']
            image = secure_filename(img.filename)
            query = 'select * from product where pid=%s'
            s = (str(id))
            v = select1(query, s)
            if v[1] == name and v[2] == description and str(v[3]) == price and str(v[4]) == quantity and str(
                    v[5]) == image:
                return '''<script>alert("No Changes found for update");window.location="/productMan"</script>'''
            elif v[1] == name and v[2] == description and str(v[3]) == price and str(v[4]) == quantity and image == '':
                return '''<script>alert("No Changes found for update");window.location="/productMan"</script>'''
            elif image != '':
                img.save(os.path.join("./static/product/", image))
                q = 'update product set product_name=%s,description=%s,price=%s,quantity=%s,image=%s where pid=%s'
                values = (name, description, price, quantity, image, id)
                insert(q, values)
            else:
                q = 'update product set product_name=%s,description=%s,price=%s,quantity=%s where pid=%s'
                values = (name, description, price, quantity, id)
                insert(q, values)
            return '''<script>alert("Product Details Updated!");window.location="/productMan"</script>'''
        except Exception:
            return '''<script>alert("Product not Updated!");window.location="/productMan"</script>'''
    else:
        return redirect('/')


@objnam.route('/prod_delete', methods=["get", "post"])
def prod_delete():
    if 'lidm' in session:
        id = request.args.get('id')
        query = "delete from product where pid=%s"
        s = (str(id))
        insert(query, s)
        return '''<script>alert("Product Deleted");window.location="/productMan"</script>'''
    else:
        return redirect('/')


@objnam.route('/cart')
def cart():
    if 'lidm' in session:
        return render_template('cartlist.html')
    else:
        return redirect('/')


@objnam.route('/cartview')
def cart_view():
    if 'lidm' in session:
        q = "SELECT `cart`.`cart_id`,`user`.`fname`,`user`.`lname`,`user`.`post`,`user`.`place`,`user`.`pin`,`cart`.`uid` FROM `cart` JOIN `user` ON `user`.`lid`=`cart`.`uid` JOIN `cart_details` ON `cart_details`.`cart_id`=`cart`.`cart_id` WHERE `cart_details`.`status`='cartlist' GROUP BY `cart_details`.`cart_id` ORDER BY `cart_id`;"
        s = selectAll(q)
        return render_template('cartlist.html', full=s)
    else:
        return redirect('/')


@objnam.route('/cartsearch', methods=['post'])
def cartsearch():
    if 'lidm' in session:
        code = request.form['textfield']
        q = "SELECT `cart`.`uid`,`cart`.`cart_id`,`user`.`fname`,`user`.`lname`,`user`.`post`,`user`.`place`,`user`.`pin` FROM `user` JOIN `cart` ON `cart`.`uid`=`user`.`lid` JOIN `cart_details` ON `cart_details`.`cart_id`=`cart`.`cart_id` WHERE `cart`.`cart_id`=" + \
            str(code) + " AND `cart_details`.`status`='cartlist' GROUP BY `cart_details`.`cart_id`"
        s = selectAll(q)
        return render_template('cartlist.html', search=s, val=code)
    else:
        return redirect('/')


@objnam.route('/cartlist2', methods=['post', 'get'])
def cartlist2():
    if 'lidm' in session:
        uid = request.args.get('id')
        cid = request.args.get('cid')
        q = "SELECT `product`.`product_name`,`cart_details`.`quantity`,`product`.`price`,`cart_details`.`quantity`*`product`.`price`,`cart`.`total_amount`,`cart_details`.`cart_id`,`product`.`pid` FROM `product` JOIN `cart_details` ON `product`.`pid`=`cart_details`.`product_id` JOIN `cart` ON `cart`.`cart_id`=`cart_details`.`cart_id` WHERE `cart`.`uid`='" + \
            str(uid) + "' and `cart`.`cart_id`='" + str(cid) + "'"
        s = selectAll(q)
        query = "SELECT SUM(`cart_details`.`quantity`*`product`.`price`) AS `total_amount` FROM `product` JOIN `cart_details` ON `product`.`pid`=`cart_details`.`product_id` JOIN `cart` ON `cart`.`cart_id`=`cart_details`.`cart_id` WHERE `cart`.`uid`='" + \
                str(uid) + "' and `cart`.`cart_id`='" + str(cid) + "'"
        m = selectAll(query)
        return render_template('viewCartlist.html', res=s, val=m)
    else:
        return redirect('/')


@objnam.route('/cartremove', methods=["get", "post"])
def cartremove():
    if 'lidm' in session:
        id = request.args.get('id')
        query = "UPDATE `cart_details` SET `status`='done' WHERE `cart_id`=%s;"
        s = (str(id))
        insert(query, s)
        for i in request.form.getlist('pid'):
            for j in request.form.getlist('qty'):
                q = "UPDATE `product` SET `quantity`=`quantity`-%s WHERE `pid`=%s;"
                values = (j, i)
                insert(q, values)
        return '''<script>alert("Cart Finished");window.location="/cart"</script>'''
    else:
        return redirect('/')


@objnam.route('/logout')
def logout():
    session.clear()
    return '''<script>alert("Logged Out Successfully! Thank you for Visiting");window.location="/"</script>'''


if __name__ == '__main__':
    objnam.run(debug=True)

from flask import Flask, request
from flask import render_template
from flask import redirect, url_for
from utils import *
import psycopg2
import psycopg2.extras

app = Flask(__name__)


@app.route("/")
def show_menu():
    return render_template("index.html")


@app.route("/newproducts", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        descrip = request.form['descrip']
        cant = request.form['cant']
        dictionary = {"name2": name, "descrip2": descrip, "cant2": cant}
        insert(dictionary)
    return render_template("new_products.html")


@app.route("/newcustomers", methods=['POST', 'GET'])
def register2():
    if request.method == 'POST':
        name = request.form['name']
        rfc = request.form['rfc']
        city = request.form['city']
        dire = request.form['dire']
        dictionary2 = {"name1": name, "rfc1": rfc, "city1": city, "dire1": dire}
        insert2(dictionary2)
    return render_template("new_customers.html")


@app.route("/funcion/<id>", methods=['POST', 'GET'])
def fc(id):
    lista = request.form.getlist('ids_select', type=int)
    insert_product_customer(id, lista)
    print(lista)
    return redirect(url_for('show_menu'))


@app.route("/assignation")
def get_data_cus():
    try:
        # remove()
        lista = graphical_customerspro()
        conn = connection_db()
        # conn.row_factory = sqlite3.Row
        # c = conn.cursor()
        c = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        c.execute(
            "select c.id, c.nombre as cliente, c.rfc, c.ciudad,c.direccion," \
            + "count(p.nombre) as producto , sum(p.cantidad) as total from " \
            + "custom_prod as cp left join  customer as c on  c.id = cp.customer_id " \
            + "left join producto as p on cp.product_id = p.id group by cliente, c.id"
        )
        rows_customer = c.fetchall()
        return render_template("assignation.html", rows=rows_customer, lista=lista)
    except Exception as e:
        print(e)
    finally:
        conn.close()


@app.route("/products")
def get_data_pro():
    try:
        conn = connection_db()
        # conn.row_factory = sqlite3.Row
        # c = conn.cursor()
        c = conn.cursor(cursor_factory=psycopg2.extras.DictRow)
        # remove()
        # bar = graphical_productsb()
        # circle = graphical_product()

        c.execute("select * from producto")
        rows_products = c.fetchall()
        return render_template("products.html", rows_p=rows_products)
    except Exception as e:
        print(e)
    finally:
        conn.close()



@app.route("/customers")
def get_data_customer():
    try:
        conn = connection_db()
        c = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        c.execute("select * from customer")
        rows_customer = c.fetchall()
        return render_template("customers.html", rows_c=rows_customer)
    except Exception as e:
        print(e)
    finally:
        conn.close()


@app.route('/delete/<id>', methods=['GET', 'POST'])
def delete_product(id):
    try:
        conn = connection_db()
        c = conn.cursor()
        c.execute(f"""DELETE FROM producto WHERE id = {id}""")
        conn.commit()
        print("Se elimino")
    except Exception as e:
        print(e)
    finally:
        conn.close()
    return redirect(url_for('get_data_pro'))


@app.route('/deletec/<id>', methods=['GET', 'POST'])
def delete_costomer(id):
    try:
        conn = connection_db()
        c = conn.cursor()
        c.execute(f"""DELETE FROM customer WHERE id = {id}""")
        conn.commit()
        print("Se elimino")
    except Exception as e:
        print(e)
    finally:
        conn.close()
    return redirect(url_for('get_data_customer'))


@app.route('/edit/<id>', methods=['POST', 'GET'])
def get_product(id):
    try:
        conn = connection_db()
        c = conn.cursor()
        c.execute(f"""SELECT * FROM producto WHERE id = {id}""")
        data = c.fetchall()
        conn.close()
        print(data[0])

    except Exception as e:
        print(e)
    finally:
        conn.close()
    return render_template('products_update.html', product=data[0])


@app.route('/update', methods=['POST'])
def update_product():
    try:
        if request.method == 'POST':
            idpro = request.form['idp']
            name = request.form['name']
            descrip = request.form['descrip']
            cant = request.form['cant']
            dictionary_product = {"name2": name, "descrip2": descrip, "cant2": cant}
            conn = connection_db()
            c = conn.cursor()
            c.execute(f"""UPDATE producto SET nombre = {name}, descripcion = {descrip}, 
                            cantidad = {cant} WHERE id = {idpro}""")
            conn.commit()
            print("Datos guardados")
    except Exception as e:
        print(e)
    finally:
        conn.close()
    return redirect(url_for('show_menu'))


@app.route('/editcust/<id>', methods=['POST', 'GET'])
def get_customer(id):
    try:
        sqli_product_rest = get_product_p(id)
        sqli_pdc = get_product_cust(id)
        conn = connection_db()
        # c = conn.cursor()
        c = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        c.execute(f"""SELECT * FROM customer WHERE id ={id}""")
        data = c.fetchall()
        conn.close()
        print(data[0])
        return render_template('customer_update.html', customert=data[0],
                               rows=sqli_product_rest, rows_pd=sqli_pdc)
    except Exception as e:
        print(e)
    finally:
        conn.close()


@app.route('/updatec/<id>', methods=['POST'])
def update_customer(id):
    try:
        if request.method == 'POST':
            name = request.form['name']
            rfc = request.form['rfc']
            city = request.form['city']
            dire = request.form['dire']
            print(name)
            conn = connection_db()
            c = conn.cursor()
            c.execute(f""" UPDATE customer SET nombre = '{name}', rfc ='{rfc}', ciudad = '{city}' , direccion = '{dire}'  WHERE id = {id} """)

            conn.commit()
            print("Datos guardados")
    except Exception as e:
        print(e)
    finally:
        conn.close()
    return redirect(url_for('show_menu'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

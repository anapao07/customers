
import matplotlib
import matplotlib.pyplot as plt
from flask import render_template
import numpy as np	
from datetime import datetime
import glob
import os
import sqlite3 


def insert_product_customer(id,lista): 
     try:
        conn = connection_db()
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        for ids in lista:
            c.execute(f"""insert  into custom_prod(product_id, customer_id) 
                       values ({ids},{id})""")
            print("insertado")   
            conn.commit()
     except Exception as e:
         print(e)
     finally:
         conn.close()  

def get_product_cust(id):
    try:
        conn = connection_db()
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        sentencia = "select c.id as idcliente, p.id, p.nombre as producto " \
        +"from custom_prod AS cp left join  customer as c on " \
        +"c.id = cp.customer_id left join producto as p " \
        +"on cp.product_id = p.id where c.id = ?;"
        c.execute(sentencia, [id])
        rows_prod_cust = c.fetchall()
        return rows_prod_cust
    except Exception as e:
        print(e)
    finally:                                                                
        conn.close()

def get_product_p(id):
    try:
        conn = connection_db()
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        sentencia = "SELECT id,nombre FROM producto WHERE id NOT IN (" \
        +"SELECT product_id FROM custom_prod WHERE customer_id = ?)"
        c.execute(sentencia, [id])
        rows_rest = c.fetchall()
        return rows_rest
    except Exception as e:
        print(e)
    finally:                                                                
        conn.close()        

def get_data_cp():
    try:
        conn = connection_db()
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("select c.nombre as cliente, p.nombre as producto " \
        +"from custom_prod AS cp left join  customer as c " \
        +"on  c.id = cp.customer_id left join producto as p " \
        +"on cp.product_id = p.id")
        row_cp = c.fetchall()
        return render_template("assignation.html",rows = row_cp)

    except Exception as e:
        print(e)
    finally:                                                                
        conn.close()

def insert(dictionary):
    try:
        conn = connection_db()
        c = conn.cursor()
        nombre = dictionary['name2']
        descripcion = dictionary['descrip2']
        cantidad = dictionary['cant2']
        c.execute(f"""INSERT INTO producto(nombre,descripcion,cantidad) 
                    values ('{nombre}','{descripcion}',{cantidad})""")
        conn.commit()
        
    except Exception as e:
        print(e)
    finally:
        conn.close()
    
    return render_template("view.html")


def insert2(dictionary2):
    try:
        conn = connection_db()
        c = conn.cursor()
        nombre = dictionary2['name1'] 
        rfc = dictionary2['rfc1']
        ciudad = dictionary2['city1']
        direccion = dictionary2['dire1']
        c.execute(f"""INSERT INTO customer(nombre,rfc,ciudad,direccion)
                    values ('{nombre}','{rfc}','{ciudad}','{direccion}')""")
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        conn.close()
    return render_template("view2.html")

def connection_db():
    conn = sqlite3.connect('sql/producto.db')
    return conn



def graphical_product():
    try:
        dateTimeObj = datetime.now()
        conn = connection_db()
        conn.row_factory = lambda cursor, row: row[0]
        c = conn.cursor()
        cantidad = c.execute('select cantidad value from producto').fetchall()
        print(cantidad)
        c = c.execute("SELECT nombre FROM producto")
        lab =c.fetchall()
        print(lab)
        sizes = cantidad
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes,labels=lab,autopct='%1.0f%%',
                shadow=True, startangle=100)
        ax1.axis('equal')  
        timeStr = dateTimeObj.strftime("%H:%M:%S")
        print('Current Timestamp : '+ timeStr)     
        nombre = "products" + timeStr  +".png"
        plt.savefig("static/image/"+ nombre)
        plt.show()
        return nombre
    except Exception as e:
        print(e)
    finally:
        conn.close()

def graphical_productsb():
    try:
        dateTimeObj = datetime.now()
        conn = connection_db()
        conn.row_factory = lambda cursor, row: row[0]
        c = conn.cursor()
        cantidad = c.execute('select cantidad value from producto').fetchall()
        c = c.execute("SELECT nombre FROM producto")
        lab =c.fetchall()
        labels = lab
        products = cantidad
        x = np.arange(len(labels))  # the label locations
        width = 0.35  # the width of the bars
        fig, ax = plt.subplots()
        rects1 = ax.bar(x - width/2, products, width, label='Productos')
        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('Cantidad')
        ax.set_title('Productos')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()
        timeStr = dateTimeObj.strftime("%H:%M:%S")
        print('Current Timestamp : '+ timeStr)
        nombre = "productbarra" + timeStr  +".png"
        for rect in rects1:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
            xy=(rect.get_x() + rect.get_width() / 2, height),
            xytext=(0, 3),  # 3 points vertical offset
            textcoords="offset points",
            ha='center', va='bottom')
            fig.tight_layout()
            plt.savefig("static/image/"+ nombre)
        return nombre
    except Exception as e:
        print(e)
    finally:
        conn.close()

def graphical_customerspro():
    try:
        conn = connection_db()
        c = conn.cursor()
        resutados_cliente_producto = c.execute("""SELECT c.nombre as cliente,
                p.nombre as producto, p.cantidad FROM custom_prod AS cp
                LEFT JOIN  customer as c on c.id = cp.customer_id 
                LEFT JOIN producto as p on cp.product_id = p.id""").fetchall()
        productos = c.execute("SELECT nombre FROM producto").fetchall()
        l =[num for elem in productos for num in elem]

        clientes = c.execute("SELECT nombre FROM customer").fetchall()
        # Generador que convierte las tuplas en lista 
        lista_todos_productos = [value[0] for value in productos]
        cliente_producto = {}
        results = {}
        for cliente in clientes:
            cliente_producto[cliente[0]] = None
            results[cliente[0]] = None 
        for cliente in cliente_producto.keys():
            cliente_producto[cliente] = dict.fromkeys(lista_todos_productos, 0)
        for value in resutados_cliente_producto:
            cliente_producto[value[0]][value[1]] = value[2] 
        values_clientes = {}    
        for value,key in zip(cliente_producto.values(), cliente_producto.keys()):
            values_clientes[key] = list(value.values())
            
        category_names = l
        results = values_clientes
        nombre = survey(results, category_names)
        return nombre
    except Exception as e:
        print(e)
    finally:
        conn.close()   

def survey(results, category_names):
    dateTimeObj = datetime.now()
    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    category_colors = plt.get_cmap('RdYlGn')(
    np.linspace(0.15, 0.85, data.shape[1]))
    fig, ax = plt.subplots(figsize=(15, 8))
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.sum(data, axis=1).max())
    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        ax.barh(labels, widths, left=starts, height=0.6,
                label=colname, color=color)
        xcenters = starts + widths / 2
        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        for y, (x, c) in enumerate(zip(xcenters, widths)):
            ax.text(x, y, str(int(c)), ha='center', va='center',
                    color=text_color)
    ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
              loc='lower left', fontsize='small')
    timeStr = dateTimeObj.strftime("%H:%M:%S")
    print('Current Timestamp : '+ timeStr)     
    nombre = "productlista" + timeStr  +".png"
    plt.savefig("static/image/"+ nombre)          
    return nombre

def remove():
    filelist=glob.glob("static/image/*.png")
    for file in filelist:
        os.remove(file)


#!/usr/bin/python
from cgi import print_arguments
import psycopg2
from bd.config import config
from modules.validator import CheckEmail, CheckPhoneNumber, CheckDocument

def connect():
    """ Connect a BD PostgreSQL """
    conn = None
    try:
        # Leer parámetros de conexión
        params = config()
        # Conectarse al servidor de BD
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        # Crear un cursor
        cur = conn.cursor()
	# Ejecutar la sentencia SQL 
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
        # Desplegar la versión de PostgreSQL
        db_version = cur.fetchone()
        print(db_version)
       
	# Cerrar la comunicación con POstgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"WB", {error})
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def showClients():
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT cli_id, cli_nombres, cli_direccion, cli_email, cli_estado FROM cliente order by cli_id")
        rows = cur.fetchall()
        for row in rows:
            print(row)
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"WB", {error})
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def insertClient(nombres, direccion, email, telefono, cedula):
    conn = None
    idCliente = 0
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        #Proceso de consulta de máximo 
        maximoRegistros = "SELECT max(cli_id)+1 as cantidad FROM cliente"
        cur.execute(maximoRegistros)
        maxReg = cur.fetchone()
        maxRegCantidad = int(maxReg[0])

        #Proceso de inserción de datos
        sentenciaSql = f"INSERT INTO cliente (cli_id, cli_nombres, cli_direccion, cli_email, cli_telefono, cli_cedula, cli_estado) VALUES ({maxRegCantidad},'{nombres}', '{direccion}', '{email}', '{telefono}', '{cedula}', 'A')" 
        cur.execute(sentenciaSql)
        conn.commit()
        print("Nuevo cliente creado")
    except (Exception, psycopg2.DatabaseError) as error:    
        print(f"WB", {error})
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def updateEmailClient(email, idCliente):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        sentenciaSql = f"UPDATE cliente SET cli_email = '{email}' WHERE cli_id = {idCliente}"
        cur.execute(sentenciaSql)
        conn.commit()
        print("Cliente actualizado")
    except (Exception, psycopg2.DatabaseError) as error:    
        print(f"WB", {error})
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def deactivateClient(idCliente):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        sentenciaSql = f"UPDATE cliente SET cli_estado = 'I' WHERE cli_id = {idCliente}"
        cur.execute(sentenciaSql)
        conn.commit()
        print("Cliente desactivado")
    except (Exception, psycopg2.DatabaseError) as error:    
        print(f"WB", {error})
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def activateClient(idCliente):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        sentenciaSql = f"UPDATE cliente SET cli_estado = 'A' WHERE cli_id = {idCliente}"
        cur.execute(sentenciaSql)
        conn.commit()
        print("Cliente activado")
    except (Exception, psycopg2.DatabaseError) as error:    
        print(f"WB", {error})
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def createClient():
    nombres = str(input("Ingrese el nombre del cliente: "))
    direccion = str(input("Ingrese su dirección: "))
    email = str(input("Ingrese su email: "))
    telefono = str(input("Ingrese su teléfono: "))
    cedula = str(input("Ingrese su cédula: "))
    if (CheckEmail(email) and CheckPhoneNumber(telefono) and CheckDocument(cedula)):
        insertClient(nombres, direccion, email, telefono, cedula)
    else:
        print("Datos inválidos, por favor verifique y vuelva a intentarlo")
    # insertClient(nombres, direccion, email, telefono, cedula)

def choseMenu():
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        Id = "Id"
        Categoria = "Categoría"
        cur.execute("SELECT cat_id, cat_nombre FROM categoria")
        rows = cur.fetchall()
        print(f"{Id:2}        {Categoria:10}")
        print("-"*20)
        for row in rows:
            print(f"{row[0]:2}        {row[1]:10}")
        
        idCategoria = int(input("Ingrese el id de la categoría: "))
        print("\nLos productos el menú de acuerdo a la categoría seleccionada son: \n")	
        choseProduct(idCategoria)

    except (Exception, psycopg2.DatabaseError) as error:    
        print(f"Cat", {error})
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def choseProduct(idCategoria: int):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        Id = "Id"
        Nombre = "Nombre"
        Precio = "Precio"

        cur.execute(f"SELECT men_id, men_nombre, men_precio FROM menu WHERE cat_id = {idCategoria} and men_estado='A'")
        rows = cur.fetchall()
        print(f"{Id:1}       {Nombre:35}       {Precio:10}")
        print(61*"-")
        for row in rows:
            print(f"{row[0]:2}       {row[1]:35}       {row[2]:10}")
        
        seleccion = False
        Total = 0
        DetallePedido = []
        while seleccion == False:
            idProducto = int(input("\nIngrese el id del producto: "))
            Cantidad = int(input("\nIngrese la cantidad del producto seleccionado: "))
            SubTotal = Cantidad * rows[idProducto-rows[0][0]][2]
            # DetallePedido = {"Producto": rows[idProducto-rows[0][0]][1], "Cantidad": Cantidad, "Precio": rows[idProducto-rows[0][0]][2], "SubTotal": SubTotal}	
            DetallePedido.append([rows[idProducto-rows[0][0]][1], Cantidad, rows[idProducto-rows[0][0]][2], SubTotal])
            Total = Total + SubTotal
            idProducto = int(input("\nPara Finalizar su pedido digite 1, si desea agregar más productos digite 2: "))
            if idProducto == 1:
                seleccion = True
            elif idProducto == 2:
                seleccion = False
        print("\nEl detalle del pedido es el siguiente: \n")
        for i in range(len(DetallePedido)):
            print(f"{DetallePedido[i][0]:35}       {DetallePedido[i][1]:10}       {DetallePedido[i][2]:10}       {DetallePedido[i][3]:10}")
        print("\nEl total a pagar es: ", Total)
        # choseClient(idProducto)

    except (Exception, psycopg2.DatabaseError) as error:    
        print(f"Menu", {error})
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def deleteFactura(id_factura):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        sentenciaSql = f"delete from factura WHERE fac_id = {id_factura}"
        cur.execute(sentenciaSql)
        conn.commit()
        print("Factura eliminada")
    except (Exception, psycopg2.DatabaseError) as error:    
        print(f"WB", {error})
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def test():
    # print(CheckEmail("Test"))
    # print(CheckEmail("Test@"))
    print(CheckEmail(5.25))
    # print(CheckEmail("Test@gmail.net"))

if __name__ == '__main__':
     choseMenu()
    # connect()
    # showClients()
    # createClient()
    # createClient("José", "Calle 2", "jose@gmai/*//com", "1234567", "1234567890")
    # updateEmailClient("ottovera@gmail.com", 6)	
    # test()
    # deactivateClient(6)
    # activateClient(6)
    # showClients()
    # deleteFactura(1)   
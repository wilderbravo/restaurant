import psycopg2
from bd.config import config
from modules.validator import CheckEmail, CheckPhoneNumber, CheckDocument

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
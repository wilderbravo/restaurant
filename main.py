#!/usr/bin/python
import psycopg2
from bd.config import config

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
        cur.execute("SELECT cli_id, cli_nombres, cli_direccion, cli_email FROM cliente order by cli_id")
        rows = cur.fetchall()
        for row in rows:
            print(row)
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"WB", {error})
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def createClient(nombres, direccion, email, telefono, cedula):
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
        sentenciaSql = f"INSERT INTO cliente (cli_id, cli_nombres, cli_direccion, cli_email, cli_telefono, cli_cedula) VALUES ({maxRegCantidad},'{nombres}', '{direccion}', '{email}', '{telefono}', '{cedula}')" 
        cur.execute(sentenciaSql)
        conn.commit()
        print("Nuevo cliente creado")
    except (Exception, psycopg2.DatabaseError) as error:    
        print(f"WB", {error})
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

if __name__ == '__main__':
    # connect()
    showClients()
    # createClient("José", "Calle 2", "jose@gmai.com", "1234567", "1234567890")
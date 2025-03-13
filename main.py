import sqlite3
import pandas as pd
import random
import os
import time

def getColumnNames(table:str):
    with sqlite3.connect('Iot.db') as conn:
        query = f'''
        SELECT * FROM {table}
        '''
        result = pd.read_sql_query(query, conn)
        equiposColumnNames = result.columns.tolist()
        return equiposColumnNames

tables = {
    'equipos': None,  
    'proveedores': None,
    'almacenadores': None
}

responses = {
    'a': 'Refrigerador',
    'b': 'Microondas',
    'c': 'Lavadora',
    'd': 'Secadora',
    'e': 'Cafetera',
    'f': 'Aspiradora',
    'g': 'Television',
    'h': 'Lampara',
    'i': 'Computadora',
    'j': 'Tostadora'
}

responses2 = {
    '1': 'Refrigerador',
    '2': 'Microondas',
    '3': 'Lavadora',
    '4': 'Secadora',
    '5': 'Cafetera',
    '6': 'Aspiradora',
    '7': 'Television',
    '8': 'Lampara',
    '9': 'Computadora',
    '10': 'Tostadora'
}

for tableName in tables:
    tables[tableName] = getColumnNames(tableName)
    
    
class Equipo:
    def getData(self, data, nombreEquipo):
        with sqlite3.connect('Iot.db') as conn:
            cursor = conn.cursor()
            query = f'''
            SELECT {data} FROM equipos
            WHERE tipo_equipo == '{nombreEquipo}'
            '''
            cursor.execute(query)
            result = cursor.fetchall()
            realValue = result[0][0]
            return realValue
        
    def lowerQuantity(self, query): 
        with sqlite3.connect('Iot.db') as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            
    def callProvider(self, nombreEquipo):
        os.system('clear')
        print('Encontrando proveedor correspondiente...')
        time.sleep(random.randint(1,5))
        with sqlite3.connect('Iot.db') as conn:
            cursor = conn.cursor()
            query = f'''
            SELECT  tipo_equipo, id_proveedor, nombre_proveedor FROM equipos
            JOIN proveedores 
            ON equipos.id_equipo = proveedores.id_equipo
            WHERE equipos.tipo_equipo == '{nombreEquipo}'
            '''
            result = pd.read_sql_query(query, conn)
            print(result)
            time.sleep(3.5)
            
            inverse = {value:key for key,value in responses2.items()}
            actual = inverse[nombreEquipo]
            
            query2 = f'''
            UPDATE proveedores
            SET solicitudes = solicitudes +1, pedidos = pedidos +1 
            WHERE id_equipo = {actual}
            '''
            cursor.execute(query2)
            conn.commit()
            
            print('\nCambios guardados en la base de datos.')
            query3= f'''
            SELECT id_proveedor, nombre_proveedor, solicitudes, pedidos FROM proveedores 
            JOIN equipos
            ON equipos.id_equipo = proveedores.id_equipo
            WHERE equipos.tipo_equipo = '{nombreEquipo}'
            '''
            result2 = pd.read_sql_query(query3,conn)
            print(f'\n{result2}')
            time.sleep(3.5)
            
            os.system('clear')
            print('CONEXIÓN EXITOSA CON EL PROVEEDOR\n')
            time.sleep(2)
            os.system('clear')
            print('Buscando conexión con el almacenador...')
            time.sleep(random.randint(3,6))
            os.system('clear')
            print("ALMACENADOR CORRESPONDIENTE ENCONTRADO")
            query4 = f'''
            SELECT nombre_almacenador, almacenadores.id_almacenador
            FROM almacenadores 
            JOIN proveedores
            ON almacenadores.id_almacenador = proveedores.id_almacenador
            WHERE proveedores.id_equipo = {actual}
            '''
            result3 = pd.read_sql_query(query4, conn)
            print(result3)
            time.sleep(3.5)
            query5 = f'''
            UPDATE almacenadores
            SET pedidos = pedidos +1, entregas = entregas +1
            WHERE id_almacenador = {actual}
            
            '''
            cursor.execute(query5)
            conn.commit()
            print('\nCambios guardados en la base de datos.')
            time.sleep(2.5)
            os.system('clear')
            print('CONEXIÓN EXITOSA CON EL ALMACENADOR\n')
            time.sleep(4)
            os.system('clear')
            query6 = f'''
            UPDATE equipos
            SET cantidad = cantidad + 10
            WHERE id_equipo = {actual}
            
            '''
            cursor.execute(query6)
            conn.commit()
            
            print('OPERACIÓN EXITOSA.\n')
            time.sleep(2)
            os.system('clear')
            print(f'EL EQUIPO {nombreEquipo} volvió a surtirse a su máximo')
            time.sleep(4)
            
#------------------------------------------------------#

def main():
    while True:
        os.system('clear')
        print('''
\033[34mMENU GENERAL DE LOS EQUIPOS INTELIGENTES\033[0m

- Elige un equipo inteligente para interactuar con él:

    a) Refrigerador
    b) Microondas
    c) Lavadora
    d) Secadora
    e) Cafetera
    f) Aspiradora
    g) Televisión
    h) Lámpara
    i) Computadora
    j) Tostadora

Escribe la letra de tu opción a continuación:''')

        response = input('''\033[34m= \033[0m''').lower()

        if response.isalpha():
            os.system('clear')
            equipoEscgido = responses[response]
            equipoActual = Equipo()
            print(f'''
\033[34mEscoge la opción que quieras realizar:\033[0m 

    Equipo escogido: \033[32m{equipoEscgido}\033[0m

    a) Ver datos del equipo
    b) Usar el equipo (consumir las unidades)

Escribe la letra de tu opción a continuación: 
              ''')
            response2 = input('''\033[34m= \033[0m''').lower()
        else:
            continue
        if response2.isalpha():
            os.system('clear')
            if response2 == 'a': 
                print(f'''
\033[34mEscoge la opción que quieras realizar:\033[0m

    Equipo: \033[32m{equipoEscgido}\033[0m

    a) Ver ID del equipo.
    b) Ver la dirección IP del equipo.
    c) Ver la cantidad disponible.
    d) Ver sus unidades mínimas requeridas.

Escribe la letra de tu opción a continuación: 
                      ''')
                response3 = input('''\033[34m= \033[0m''').lower()
                if response3 == 'a':
                    out = equipoActual.getData('id_equipo',     equipoEscgido)
                    print(f'\nEl id del equipo es: {out}')
                elif response3 == 'b':
                    out = equipoActual.getData('direccion_ip',  equipoEscgido)
                    print(f'\nLa dirección IP del equipo es: {out}')
                elif response3 == 'c':
                    out = equipoActual.getData('cantidad',  equipoEscgido)
                    print(f'\nLa cantidad disponible del equipo es: {out}')
                elif response3 == 'd':
                    out = equipoActual.getData('control',   equipoEscgido)
                    print(f'\nLa cantidad mínima requerida del equipo es: {out}')
                else:
                    print("Elige una opción válida")
                    
                print('\nPresiona enter para regresar')
                if input():
                    continue
                
            
            elif response2 == 'b':
                if (equipoActual.getData('cantidad', equipoEscgido)) == 0:
                    print("No hay unidades disponibles para consumir")
                    print('\n¿Deseas llamar al proveedor para volver a surtir los productos?')
                    call = input("= ").lower().replace("í", "i")
                    if call == 'si':
                        equipoActual.callProvider(equipoEscgido)
                    
                
                with sqlite3.connect('Iot.db') as conn:
                    cursor = conn.cursor()
                    query = f'''
                    SELECT cantidad FROM equipos
                    WHERE tipo_equipo = '{equipoEscgido}'
                    '''
                    cursor.execute(query)
                    result = cursor.fetchall()
                    cantidad = result[0][0]
                
                gasto = random.randint(1, cantidad)
                query = f'''
                UPDATE equipos
                SET cantidad = cantidad - {gasto} 
                WHERE tipo_equipo == '{equipoEscgido}'
                '''
                equipoActual.lowerQuantity(query)
                
                print(f'Se han consumido \033[31m{gasto}\033[0m unidades de producto del equipo\n')
                print(f'El control del equipo es:\033[32m {equipoActual.getData('control', equipoEscgido)}\033[0m\n')
                print(f'La cantidad actual es:\033[34m {equipoActual.getData('cantidad', equipoEscgido)}\033[0m\n')
                
                if (equipoActual.getData('cantidad', equipoEscgido)) > (equipoActual.getData('control', equipoEscgido)):
                    print('El equipo aún tiene unidades suficientes. No requiere voler a surtirse.')
                else:
                    print('El equipo ya no tiene unidades suficientes. Requiere voler a surtirse\n')
                    print('¿Deseas llamar al proveedor para volver a surtir los productos?')
                    call = input("= ").lower().replace("í", "i")
                    if call == 'si':
                        equipoActual.callProvider(equipoEscgido)
                    else:
                        print('\nNo se ha realizado ninguna acción')
                        print('\nPresiona enter para regresar')
                        if input():
                            continue
                
if __name__ == '__main__':
    main()
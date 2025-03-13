import sqlite3
import pandas as pd

#-----------------------------------------------------------
#Vista de desarrollador
#    '1': 'Refrigerador',
#    '2': 'Microondas',
#    '3': 'Lavadora',
#    '4': 'Secadora',
#    '5': 'Cafetera',
#    '6': 'Aspiradora',
#    '7': 'Television',
#    '8': 'Lampara',
#    '9': 'Computadora',
#    '10': 'Tostadora'
#


#Agregar cantidad

def modificarCantidad():
    with sqlite3.connect('Iot.db') as conn:
        cursor = conn.cursor()
        query = f'''
        UPDATE equipos
        SET cantidad = {2}
        WHERE id_equipo = {1}
        '''
        cursor.execute(query)
        conn.commit()
    
    
#Establecer control
def modificarControl():
    with sqlite3.connect('Iot.db') as conn:
        cursor = conn.cursor()
        query = f'''
        UPDATE equipos
        SET control = {3}
        WHERE id_equipo = {1}
        '''
        cursor.execute(query)
        conn.commit()
    

def reiniciarProveedores():
    with sqlite3.connect('Iot.db') as conn:
        cursor = conn.cursor()
        query = '''
        UPDATE proveedores
        SET solicitudes = 0, pedidos = 0    
        '''
        cursor.execute(query)
        conn.commit()

def reiniciarAlmacenadores():
    with sqlite3.connect('Iot.db') as conn:
        cursor = conn.cursor()
        query = '''
        UPDATE almacenadores
        SET pedidos = 0, entregas = 0    
        '''
        cursor.execute(query)
        conn.commit()


 
reiniciarAlmacenadores()
reiniciarProveedores()
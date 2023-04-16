import os
import psycopg2

DROP_USER_TABLE = """ DROP TABLE IF EXISTS users"""

USER_TABLE = """ CREATE TABLE users(
id SERIAL,
username VARCHAR (50) NOT NULL,
email VARCHAR (50) NOT NULL,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)"""

def system_clear(function):
   def wrapper(connect,cursor):
      os.system('clear')
      function(connect,cursor)
      input('')
      os.system('clear')
   wrapper.__doc__ = function.__doc__
   return wrapper

@system_clear
def create_user(connect,cursor):

   """ A) Crear Usuario
   """
   username = input('Ingrese nombre del Usuario: ')
   email = input('Ingrese el email: ')
   query = "INSERT INTO users(username,email) values (%s,%s)"
   values = (username,email)
   cursor.execute(query,values)
   connect.commit()
   print('>>>>Usuario Creado con Exito')
    
@system_clear
def list_user(connect,cursor):
    """ B) Listar Usuarios
    """
    query = "select * from users"
    cursor.execute(query)
    listado = cursor.fetchall()
    for i in listado:
       print(i[0],'-',i[1],'-',i[2])
    connect.commit()
    print('>>>> Listado de Usuarios')
    pass

def user_exists(function):
   def wrapper(connect,cursor):
      id = input('>>> Ingrese el id del usuario: ')
      query = 'Select * from users where id=(%s)'
      cursor.execute(query,(id,))
      user = cursor.fetchone() #None
      if user:
        function(id,connect,cursor)
      else:
       print('Id de usuario  no valido')
   wrapper.__doc__ = function.__doc__
   return wrapper

@system_clear
@user_exists
def update_user(id,connect,cursor):
    """ C) Actualizar Usuario
    """
    username = input('Ingrese el nuevo username: ')
    email = input('Ingrese el nuevo email')
    query = 'update users set username=(%s) and email=(%s) where id = (%s)'
    values = (username,email,id,)
    cursor.execute(query,values)
    connect.commit()
    print('>>>>Usuario Actualizado con Exito')

@system_clear
@user_exists    
def delete_user(id,connect,cursor):
    """ D) Eliminar Usuario
    """
    query = 'delete from users where id = (%s)'
    cursor.execute(query,(id,))
    connect.commit()
    print('>>>>Usuario Eliminado')

@system_clear
def default(*args):
   print('Opcion no valida')

if __name__ == '__main__':
  options = {
     'a' : create_user,
     'b' : list_user,
     'c' : update_user,
     'd' : delete_user
  }  

  try: 
    connect = psycopg2.connect("postgresql://postgres:1234@localhost/proyecto")
    print('Conexion Exitosa')
    with connect.cursor() as cursor:
      
      #cursor.execute(DROP_USER_TABLE)
      #cursor.execute(USER_TABLE)

      connect.commit()

      while True:
         for function in options.values():
            print(function.__doc__)
         print('quit para salir')

         option = input('Seleccione un opcion: ').lower()

         if option == 'quit' or option == 'q':
            break
         function = options.get(option,default)
         function(connect,cursor)

  except psycopg2.OperationalError as error:
    print ('Error en la conexion')

import mysql
import mysql.connector
import os


def conecta_db():
  
  try:
    conn = mysql.connector.connect(  
        user=os.getenv('MYSQL_USER'),
        host=os.getenv('MYSQL_HOST'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DB')
    )
    print('conexao feita com sucesso')
    return conn
  
  except mysql.connector.Error as e:
    print(f'erro: {e}')



import mysql.connector

config = {
    'user': 'root',
    'password': '9wlWHkKpVCyefMpfQLCS',
    'host': 'containers-us-west-148.railway.app',
    'database': 'railway',
    'port': 5958  # Puerto predeterminado de MySQL
}
database = mysql.connector.connect(**config)

print('BBDD conectada!!')

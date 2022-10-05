from mysql.connector import ClientFlag

db_config = {
    'user': 'root',
    'password': ']#X3J6H<a09[GbUS',
    'host': '34.163.144.218',
    'client_flags': [ClientFlag.SSL],
    'ssl_ca': 'ssl/server-ca.pem',
    'ssl_cert': 'ssl/client-cert.pem',
    'ssl_key': 'ssl/client-key.pem',
    'database': 'rem_auth'
}
salt = b'$2b$12$yjghy7zSpIF.sQQJ7wUKfu'


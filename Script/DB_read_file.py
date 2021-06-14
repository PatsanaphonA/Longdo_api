import configparser

config = configparser.ConfigParser()
config.read('Database.conf')
BaseDB =config['postgresql']

host = BaseDB['host']
user = BaseDB['user']
passwd = BaseDB['passwd']
db = BaseDB['db']
port = BaseDB['port']

print('PostgreSQL configuration:')

print('Host: ' + host)
print('User: ' + user)
print('password: ' + passwd)
print('DB: ' + db)
print('port: ' + port)
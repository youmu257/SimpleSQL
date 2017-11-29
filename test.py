import os, inspect, platform
from simplesql import SimpleSQL

'''
You need create a new Database first.
This tool only test on MySQL.
If you are another database system, it may not work.
'''

# sample
# initial connect
# read simplesql/config.ini
currentPath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
if platform.system() == 'Linux':
    currentPath+"/"+'simplesql'
else:
    currentPath+"\\"+'simplesql'
conn = SimpleSQL(currentPath)
# input db connect parameter {host, port, user name, password, db}
# conn = SimpleSQL('localhost', '3306', 'user', 'password', 'mysql')


table = 'simplesql.test1'
# create table
conn.createTable(table, ['id INT NOT NULL AUTO_INCREMENT', 'name TEXT NOT NULL' , 'value INT NOT NULL' , 'date DATE NOT NULL' , 'PRIMARY KEY (id)'])

#insert sql
insertList = {'name':'user1', 'value':3345678, 'date':'20171129'}
conn.insert(table, insertList)
print(conn.selectAll(table))
 
#update sql
updateValue = {'name':'user2'}
condition = {'value':3345678}
conn.update(table, updateValue, condition)
print(conn.selectAll(table))
 
# delete sql
conn.delete(table, {'name':'user2'})
print(conn.selectAll(table))
 
#close connect
conn.closeConnect()
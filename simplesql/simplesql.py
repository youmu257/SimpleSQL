#!/usr/bin/python3
# coding=utf-8

import pymysql, os, platform, inspect
import configparser
from util import ConfigSectionMap 

class SimpleSQL:
    configName = 'config.ini'
    conn = None
    # input config.ini path or the parameter of db connect {host, port, user name, password, db}
    def __init__(self, *param):
        if len(param) == 1:
            # if input only one parameter, we let it is the path of config.ini which contain db connect parameter
            self.connectMysql(param[0])
        elif len(param) == 5:
            try:
                self.conn = pymysql.connect(host=param[0], port=int(param[1]), user=param[2], passwd=param[3], db=param[4], charset='UTF8')
                print('DB connect success!')
            except:
                print('DB connect error!')
        else :
            print('Parameter error!\nPlease input parameter for {host, port, user name, password, db} or setting config.ini.')
    
    def connectMysql(self, configDir):
        Config = configparser.ConfigParser()
    
        if platform.system() == 'Linux':
            Config.read(configDir+"/"+self.configName)
        else:
            Config.read(configDir+"\\"+self.configName)
        ConfigMap = ConfigSectionMap("DB", Config)
    
        mHost   = str(ConfigMap['host'])
        mPort   = int(ConfigMap['port'])
        mUser   = str(ConfigMap['user'])
        mPasswd = str(ConfigMap['passwd'])
        mDB     = str(ConfigMap['db'])
        
        try:
            self.conn = pymysql.connect(host=mHost, port=mPort, user=mUser, passwd=mPasswd, db=mDB, charset='UTF8')
            print('DB connect success!')
        except:
            print('DB connect error!')
            
    def closeConnect(self):
        self.conn.close()
    
    # create table with column list
    # table      : table name
    # columnList : column name and type
    def createTable(self, table, columnList):
        with self.conn.cursor() as cur:
            strColumn = ','.join(columnList)
            sql = 'CREATE TABLE IF NOT EXISTS '+table+'( '+strColumn+' ) ENGINE = InnoDB CHARACTER SET utf8 COLLATE utf8_bin;'
            cur.execute( sql )
            self.conn.commit()
            print('Create table if not exists success!')
    
    # just execute sql, so you need input complete sql command
    def execute(self, sql):
        with self.conn.cursor() as cur:
            cur.execute( sql )
            self.conn.commit()
            print('Execute sql success!')
    
    # insert data into table, ignore or update repeat data
    #  table       : table name
    #  valueDict   : column name as key and inserted value as value
    #  update(str) : if update is not null, check duplicate key to update
    #                else insert and ignore duplicate
    def insert(self, table, valueDict, update=''):
        with self.conn.cursor() as cur:
            strColumn = ",".join(valueDict.keys())
            strValue = ",".join([self.toSQLString(s) for s in valueDict.values()]) 
            sql = 'INSERT INTO '+table+' ('+strColumn+') VALUE ('+strValue+')'
            if len(update) > 0:
                sql += 'ON DUPLICATE KEY UPDATE '+update+'='+self.toSQLString(valueDict[update])
            else:
                sql = sql.replace('INSERT', 'INSERT IGNORE')
    
            cur.execute( sql )
            self.conn.commit()
    
    # get data from table, return list(dict)
    #  table     : table name
    #  condition : condition for where
    #  order     : order by some column and sort DESC
    def selectWhere(self, table, condition, order=''):
        with self.conn.cursor() as cur:
            whereStr = ",".join([str(key+'='+self.toSQLString(value)) for key, value in condition.items()])
            sql = 'SELECT * FROM '+table+' WHERE '+whereStr
            if len(order) > 0:
                sql += ' ORDER BY '+self.toSQLString(order)+' DESC'
            cur.execute(sql)
            
            results = list()
            name = [x[0] for x in cur.description]
            for row in cur:
                results.append(dict(zip(name, row)))
        return results
    
    # get data from table, return list(dict)
    #  table     : table name
    #  order     : order by some column and sort DESC
    def selectAll(self, table, order=''):
        with self.conn.cursor() as cur:
            sql = 'SELECT * FROM '+table
            if len(order) > 0:
                sql += ' ORDER BY '+self.toSQLString(order)+' DESC'
                print(sql)
            cur.execute(sql)
            
            results = list()
            name = [x[0] for x in cur.description]
            for row in cur:
                results.append(dict(zip(name, row)))
        return results
    
    # delete table by input condition
    #  table    : table name
    #  delDict : condition set, ex : {'videoId':'79800'}
    def delete(self, table, delDict):
        with self.conn.cursor() as cur:
            delStr = ",".join([str(key+'='+self.toSQLString(value)) for key, value in delDict.items()])
            cur.execute('DELETE FROM '+table+' WHERE '+delStr)
            self.conn.commit()
    
    # update table by specific condition, only for equal condition
    #  table          : table name
    #  valueDict     : the column need to update, ex : {'viewNumbers':123}
    #  conditionDict : condition set, ex : {'videoId':'79800'}
    def update(self, table, updateDict, conditionDict):
        with self.conn.cursor() as cur:
            updateStr = ",".join([str(key+'='+self.toSQLString(value)) for key, value in updateDict.items()])
            condStr = ",".join([str(key+'='+self.toSQLString(value)) for key, value in conditionDict.items()])
            cur.execute('UPDATE '+table+' SET '+updateStr+' WHERE '+condStr)
            self.conn.commit()
    
    def toSQLString(self, s):
        return ('\''+s.replace('\'','\\')+'\'') if type(s)==type('') else str(s)

if __name__ == '__main__':
    # sample
    # initial connect
    currentPath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    conn = SimpleSQL(currentPath)
#     conn = SimpleSQL('localhost', '3306', 'user', 'password', 'mysql')
    
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
    
    
    

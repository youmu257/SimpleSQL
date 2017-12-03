# SimpleSQL
This library contains common sql queries with simple function. We provide function which include create, select, update and insert, to help you running sql query with easy syntax. There are only basic sql command so that can't cover all type query. Therefore, we also provide `execute` to execute your own query.

## Installation
You can download or clone this project, and exectue `python setup.py install` to install this library.

## Functions

**Select**
```python
selectAll("tableName")
selectWhere("tableName", {'name':'user1'})
```

**Update**
```python
updateValue = {'name':'user2'}
condition = {'value':3345678}
conn.update(table, updateValue, condition)
```

**Insert**
```python
insertList = {'name':'user1', 'value':3345678, 'date':'20171129'}
insert(table, insertList)
```

**Create**
```python
createTable(table, ['id INT NOT NULL AUTO_INCREMENT', 'name TEXT NOT NULL' , 'value INT NOT NULL' , 'date DATE NOT NULL' , 'PRIMARY KEY (id)'])
```

**Execute**
```python
execute(query)
```

# To Do
1. SQL injection prevent
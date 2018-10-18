import sqlite3
from db_connection import get_db, app

def getInfoApp(appName):
	cursor = get_db().cursor()
	sql = "SELECT * FROM Apps WHERE appName=?"
	cursor.execute(sql, [appName])
	return cursor.fetchone()

def setInfoApp(appName, url, port, container):
	cursor = get_db().cursor()
	sql = "INSERT INTO Apps VALUES (?, ?, ?, ?)"
	cursor.execute(sql, [appName, url, port, container])
	get_db().commit()

def updateInfoApp(appName, url, port, container):
	cursor = get_db().cursor()
	sql = "UPDATE Apps SET url = ? , container = ? , port = ? WHERE appName=?"
	cursor.execute(sql, [url, container, port, appName])
	get_db().commit()

def getLastPort(url):
	cursor = get_db().cursor()
	sql = "SELECT port FROM Apps WHERE url = ? ORDER BY port DESC LIMIT 1"
	cursor.execute(sql, [url])
	res = cursor.fetchone()
	if res == None:
		return None
	else:
		return res[0]

import sqlite3
import pandas as pd


class DBService:
	def __init__(self, db_url):
		try:
			self.conn = sqlite3.connect(db_url)
			self.cursor = self.conn.cursor()
			self.playerTable = pd.read_sql_query('SELECT * FROM Player', self.conn)
			self.playerAttrTable = pd.read_sql_query('SELECT * FROM Player_Attributes', self.conn)
			
		except sqlite3.Error as err: 
			print("Failed to connect to db")
			print(err)

	# execute query and return as pandas dataframe
	def execute_query(self, qry_string):
		return pd.read_sql_query(qry_string, self.conn)

	def get_player_table(self):
		return self.playerTable
	
	def get_player_attr_table(self):
		return self.playerAttrTable

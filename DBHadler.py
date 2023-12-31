'''
This perticular file Handle our database functionalities.Such as creating database,
creation of new table for input data,updating data,adding new sensor
'''
import sqlite3
from utils import UtilsMaster
import csv
import pandas as pd
import os

class dbHandlerMaster(UtilsMaster):
    def __init__(self):
        
        self.DataBaseName = 'SensorData'
        self.Available_sensors = 'SENSOR'
        self.csvFile = 'PYgenerated/data.csv'
        self.output_csv = 'DBExtracted/output.csv'
        self.RegisterSensor = 'RegisterSensor(Temp)/details.csv'

    def connectWithDataBase(self):
        try:
            conn  = sqlite3.connect(self.DataBaseName+'.db')
        except ConnectionError:
            raise ConnectionError()
        return conn
        

    def createNewTable(self):
        try:
            conn  = self.connectWithDataBase()
            conn.execute('''
                CREATE TABLE IF NOT EXISTS DataFromSensor (
                         Response1 INT,
                         Response2 INT,
                         Response3 INT,
                         Response4 INT,
                         Response5 INT,
                         Date DATE

                )
                         ''')
            # conn.execute("Drop table SensorData")
            # print("Created")
            conn.commit()
            conn.close()
        except:
            print("failed")


    def insertDataIntoTable(self):
        conn = self.connectWithDataBase()
        
        with open(self.csvFile,'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader,None)
            
            for row in csv_reader:
                conn.execute('''
                INSERT INTO DataFromSensor (Response1,Response2,Response3,Response4,Response5,Date) VALUES (?,?,?,?,?,?)
                    ''',(row[0],row[1],row[2],row[3],row[4],row[5]))
            conn.commit()
            conn.close()
        

    def ExtractingDataFromDB(self):
        self.fileFromDb = 'DBExtracted/'
        self.fileName = 'output.csv'
        try:
            conn  = sqlite3.connect(self.DataBaseName+'.db')
            sqlSelect = "SELECT *  FROM DataFromSensor"
            cursor = conn.cursor()

            cursor.execute(sqlSelect)

            results = cursor.fetchall()

            #Get the headers of the csv file
            headers = [i[0] for i in cursor.description]

            #Make the CSV ouput directory
            if not os.path.isdir(self.fileFromDb):
                os.makedirs(self.fileFromDb)

            # Open CSV file for writing.
            csvFile = csv.writer(open(self.fileFromDb + self.fileName, 'w', newline=''),delimiter=',', lineterminator='\r\n',quoting=csv.QUOTE_ALL, escapechar='\\')

            # Add the headers and data to the CSV file.
            csvFile.writerow(headers)
            csvFile.writerows(results)


        except Exception as e:
            print("not extracted")
        


    def CreateNewTableForNewSensor(self,tablename):
        try:
            self.tablename = tablename
            conn  = self.connectWithDataBase()
            cursor = conn.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS {table_name} (Response1 INT,Response2 INT,Response3 INT,Response4 INT,Response5 INT,Date DATE)'.format(table_name=self.tablename))
            conn.commit()
            conn.close()
        except:
            print("failed")

        
    def DataBaseAndTableForNewSensor(self):
        sen = sqlite3.connect(self.Available_sensors+'.db')
        c = sen.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS ActiveSensors (id INTEGER,name TEXT,inputs_nodes INTEGER,establised_year YEAR,failure_percentage INT,working_capacity INTEGER,Response_time INTEGER,latency INTEGER,current_state TEXT,future_scope TEXT)')

        sen.commit()
        sen.close()
    
    def CreateCSVForNewSensor(self,id,name,inputs_nodes,establised_year,failure_percentage,working_capacity,Response_time,latency,current_state,future_scope):
        self.id=id
        self.name = name
        self.inputs_nodes = inputs_nodes
        self.establised_year = establised_year
        self.failure_percentage = failure_percentage
        self.working_capacity = working_capacity
        self.Response_time =Response_time
        self.latency = latency
        self.current_state = current_state
        self.future_scope = future_scope

        self.id=[self.id]
        self.name =[self.name]
        self.inputs_nodes =[self.inputs_nodes]
        self.establised_year =[self.establised_year]
        self.failure_percentage =[self.failure_percentage]
        self.working_capacity =[self.working_capacity]
        self.Response_time =[self.Response_time]
        self.latency =[self.latency]
        self.current_state =[self.current_state]
        self.future_scope =[self.future_scope]
        

        data = list(zip(self.id,self.name,self.inputs_nodes,self.establised_year,self.failure_percentage,self.working_capacity,self.Response_time,self.latency,self.current_state,self.future_scope))
        with open(self.RegisterSensor,'w',newline='') as csvfile:
            csv_writter = csv.writer(csvfile)
            csv_writter.writerow(['id','name','inputs_nodes','establised_year','failure_percentage','working_capacity','Response_time','latency','current_state','future_scope'])
            csv_writter.writerows(data)
    
    def InsertCSVDataToDB(self):
        sen = sqlite3.connect(self.Available_sensors+'.db')
        
        with open(self.RegisterSensor,'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader,None)
            
            for row in csv_reader:
                sen.execute(f'''
                INSERT INTO ActiveSensors (id,name,inputs_nodes,establised_year,failure_percentage,working_capacity,Response_time,latency,current_state,future_scope) VALUES (?,?,?,?,?,?,?,?,?,?)
                    ''',(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]))
                sen.execute("delete from ActiveSensors where name = '' " )
            sen.commit()
            sen.close()




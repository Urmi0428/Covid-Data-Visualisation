#Final_Project
#Team-Members:
# URMI JADEJA , ID: 4444962
# MAHMOUD HACHEM , ID: 4396805

#Import Statements
import json
from pymongo import MongoClient 
from itertools import groupby 
import pyodbc 
import sqlite3

#opening the rawjson file
with open('C:\project_files\covid_rawdata.json') as f:
    data = json.load(f)

#Outputing helpful output to user
print('*Transforming and loading Covid data now >>>>')
province_dict ={
                    "AB" :"Alberta" ,
                    "BC" : "British Columbia" ,
                    "MB" :"Manitoba",
                    "ON":"Ontario",
                    "NB":"New Brunswick",
                    "NL":"Newfoundland and Labrador",
                    "NWT":"Northwest Territories",
                    "NS":"Nova Scotia",
                    "NU":"Nunavut",
                    "PEI":"Prince Edward Island",
                    "QB":"Quebec",
                    "YT":"Yukon",
                    "SK": "Saskatchewan"
               }
#Making function to get each province with code
def province(t):
    if( t in province_dict):
        return province_dict[t]
    else:
        return t

#Making function to acsociate each code with the province
def code(t):
  keys = [k for k, v in province_dict.items() if t == v]
  if keys:
        return keys[0]
  else:
    return t

#Making empty list to append
myitems = []

#Looping through the json data
for case in data['cases']:
    if case["province"] in ["AB","Alberta" ,
                    "BC", "British Columbia" ,
                    "MB" ,"Manitoba",
                    "ON","Ontario",
                    "NB","New Brunswick",
                    "NL","Newfoundland and Labrador",
                    "NWT","Northwest Territories",
                    "NS","Nova Scotia",
                    "NU","Nunavut",
                    "PEI","Prince Edward Island",
                    "QB","Quebec",
                    "YT","Yukon",
                    "SK", "Saskatchewan"]:
            data_dict = {
           "code": code(case["province"]),
           "province": province(case["province"]),
           "stats":{"cases": case["cases"], "cumulative_cases": case["cumulative_cases"], "date_report": case["date_report"]}
                 }
            myitems.append(data_dict)

#Making function to loop through the stats only
def stat(inputCode):
    stat_list = []
    for item  in myitems:
        if inputCode == item["code"]:
            stat_list.append(item["stats"])
    return stat_list

AB = {"code":"AB","province":"Alberta","stats":stat("AB")}
BC = {"code":"BC","province":"British Columbia","stats":stat("BC")}
MB = {"code":"MB","province":"Manitoba","stats":stat("MB")}
ON = {"code":"ON","province":"Ontario","stats":stat("ON")}
NB = {"code":"NB","province":"New Brunswick","stats":stat("NB")}
NL ={"code":"NL","province":"Newfoundland and Labrador","stats":stat("NL")}
NWT ={"code":"NWT","province":"Northwest Territories","stats":stat("NWT")}
NS ={"code":"NS","province":"Nova Scotia","stats":stat("NS")}
NU ={"code":"NU","province":"Nunavat","stats":stat("NU")}
PEI ={"code":"PEI","province":"Prince Edward Island","stats":stat("PEI")}
QB ={"code":"QB","province":"Quebec","stats":stat("QB")}
YT ={"code":"YT","province":"Yukon","stats":stat("YT")}
SK ={"code":"SK","province":"Saskatchewan","stats":stat("SK")}

#Apending all the provinces dicts with its stats to a list
final = []
final.append(AB)
final.append(BC)
final.append(MB)
final.append(ON)
final.append(NB)
final.append(NL)
final.append(NWT)
final.append(NS)
final.append(NU)
final.append(PEI)
final.append(QB)
final.append(YT)
final.append(SK)

#Placing the new file to the project_files directory
with open(r"C:\project_files\covid_data.json", "w") as file:
   json.dump(final, file, indent=4)

#Outputing helpful output to user
print('*Made JSON file: c:/project_files/covid_data.json >>>>')

#Transfering the new JSON to mongoDB
myclient = MongoClient("mongodb://localhost:27017/")
db = myclient["project"]
Collection = db["covid_data"]
with open('C:\project_files\covid_data.json') as file:
    file_data = json.load(file)
print('*13 documents added to Mongo >>>>')
      
# Inserting the loaded data in the Collection
# if JSON contains data more than one entry
# insert_many is used else inser_one is used
if isinstance(file_data, list):
    Collection.insert_many(file_data)  
else:
    Collection.insert_one(file_data)

#Establishing a connection string for the SQL Conection
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server={.\sqlexpress};'
                      'Database=project;'
                      'Trusted_Connection=yes;')
#Placing it in cursor
cursor = conn.cursor()
with open(r'C:\project_files\final_MahmoudHachem_ and _UrmiJadeja.sql', 'r') as sqlfile:
    #reading the entire SQL file, placing in object
    stmt = sqlfile.read()
    #spliting the SQL statements by a semicolon at the end
    sqlCommand = stmt.split(';')
    #Looping through each statement 
    for script in sqlCommand:
        #executing each statement individually
        cursor.execute(script)
        #saving all the data initiated by the .excecute() and saving it in SQL Server
        cursor.commit()
        #print(i)

cursor.close() #Closing the cursor after statements been runned and taxed on the database   
conn.close() #closing the connection string
            
#Outputing helpful output to user
print('*Succefully loaded SQL data >>>>')

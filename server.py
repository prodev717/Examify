from fastapi import FastAPI
from pydantic import BaseModel
import json
import csv
import math

class StudentData(BaseModel):
	name:"str"
	regno:"str"
	warning:float
app = FastAPI()
dur = 60

@app.get('/duration')
def duration():
	global dur
	return {"duration":dur}

@app.post("/studentdata")
def submit(data:StudentData):
	print(data)
	with open("credresult.csv","a") as file:
		writer = csv.writer(file)
		writer.writerow([data.name,data.regno,100-math.floor(data.warning)])

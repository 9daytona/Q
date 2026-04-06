from fastapi import FastAPI
#import requests
from typing import List

app = FastAPI()

#In-memory storage (specific for prototype stage)
patients = []
observations = []

# PATIENT ENDPOINTS
@app.post("/Patient")
def create_patient(patient: dict):
    patients.append(patients)
    return patient


# FHIR_URL = "http://fhir:8080/fhir"

@app.get("/Patient")
def get_patients():
    return patients

# OBSERVATION ENDPOINTS

@app.post("/Observation")
def create_observation(obs: dict):
    observations.append(obs)
    return obs
@app.get("/Observation")
def get_observations():
    return observations

# ROOT (HEALTH CHECK)
@app.get("/")
def root():
    return {"status": "Q Care Platform API running"}
    
    
#return requests.get(f"{FHIR_URL}/Patient").json()



###################################################
## In alignment with  HL7 FHIR principles   #######
## REST endpoints, Resource-based structure #######
###################################################
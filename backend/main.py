from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Q Care Platform FHIR-compliant API")

# FHIR MODELS

class HumanName(BaseModel):
    use: Optional[str]
    family: str
    given: List[str]

class Address(BaseModel):
    line: List[str]
    city: str
    state: str
    postalCode: str
    country: str

class Patient(BaseModel):
    resourceType: str="Patient"
    id: str
    name: List[HumanName]
    gender: Optional[str]
    birthDate: Optional[str]
    address: Optional[List[Address]] =[]

class Observation(BaseModel):
    resourceType: str = "Observation"
    id: str
    status: str                     # preliminary, final
    code: dict                      # {"coding": [{...}]}
    subject: dict                   # {"reference": "Patient/{id}"}
    effectiveDateTime: str
    valueQuantity: Optional[dict]    # {"value": 88, "unit": "bpm"}

class Participant(BaseModel):
    actor: dict # {"reference": "Patient/{id}" or "Practitioner/{id}"}
    status: str # needs-action, tentative, accepted

class Appointment(BaseModel):
    resourceType: str = "Appointment"
    id: str
    status: str # fulfilled, arrived, booked
    start: str
    end: str
    participant: List[Participant]

class FamilyCall(BaseModel):
    resourceType: str = "Communication"
    id: str
    status: str
    subject: dict       # {"reference": "Patient/{id}"}
    sender: dict        # {"reference": "Practitioner/{id}"}
    recipient: dict     # {"display": "9 Daytona"}
    medium: List[dict]  # [{"coding": [{"system": "...", "code": "video"}]}]
    sent: str
    received: Optional[str]

 

# In-memory storage (specific for prototype stage)
# Local arrays to be replaced with resources 
patients: List[Patient] = []
observations: List[Observation] = []
clinical_metrics = []
envr = []
assistance_calls = []
#telehealth_app = []
appointments: List[Appointment] = []
family_comms: List[FamilyCall] = []


# PATIENT ENDPOINTS
@app.post("/Patient")
def create_patient(patient: Patient):
    patients.append(patient)
    return patient
    
@app.get("/Patient")
def get_patients():
    return patients

# OBSERVATION ENDPOINTS

@app.post("/Observation")
def create_observation(obs: Observation):
    observations.append(obs)
    return obs

@app.get("/Observation")
def get_observations():
    return observations


# ASSISTANCE CALLS ENDPOINTS
@app.get("/AssitanceCall")
def get_calls():
    return assistance_calls

@app.post("/AssistanceCall")
def create_call(call: dict):
    assistance_calls.append(call)
    return call


# CLINICAL METRICS
@app.post("/ClinicalMetric")
def create_metric(metric: dict):
    clinical_metrics.append(metric)
    return metric

@app.get("/ClinicalMetric")
def get_metrics():
    return clinical_metrics


# ENVIRONMENTAL 
@app.post("/Environment")
def create_environment(env: dict):
    envr.append(env)
    return env

@app.get("/Environment")
def get_environment();
    return envr


# APPOINTMENT ENDPOINTS
@app.post("/Appointment")
def create_appointment(appt: Appointment):
    appointments.append(appt)
    return appt

@app.get("/Appointment")
def get_appointments():
    return appointments


# FAMILY COMMS ENDPOINTS
@app.post("/Family/Calls")
def create_family_call(call: FamilyCall):
    family_comms.append(call)
    return call

@app.get("/Family/Calls")
def get_family_comms():
    return family_comms


# ROOT (HEALTH CHECK)
@app.get("/")
def root():
    return {"status": " FHIR-compliant Q Care Platform API running"}
    
    
#return requests.get(f"{FHIR_URL}/Patient").json()



###################################################
## In alignment with  HL7 FHIR principles   #######
## REST endpoints, Resource-based structure #######
###################################################
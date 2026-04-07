from fastapi import WebSocket
#import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import asyncio
from datetime import datetime
from collections import deque

app = FastAPI(title="Q Care Platform FHIR-compliant API")

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket]= []
        self.lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        async with self.lock:
            self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        async with self.lock:
            if websocket in self.active_connections:
                self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        dead_connections = []

        for connection in self.active_connections:
            try:
                #await connection.send_json(message)
                await asyncio.gather(*[conn.send_json(message) for conn in self.active_connections],
                return_exceptions=True)
            except:
                dead_connections.append(connection)
        for conn in dead_connections:
            await self.disconnect(conn)

manager = ConnectionManager()




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
    status: str                             # preliminary, final
    code: dict                              # {"coding": [{...}]}
    subject: dict                           # {"reference": "Patient/{id}"}
    effectiveDateTime: str
    category: Optional[List[dict]] = None   # Required
    device: Optional[dict] = None           # ios mobile
    valueQuantity: Optional[dict]           # {"value": 88, "unit": "bpm"}

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
#observations: List[Observation] = []
observation_buffer = deque(maxlen=1000)
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
async def ingest_observation(obs: Observation):
    # Optional FHIR timestamp normalisaton
    obs.effectiveDateTime = datetime.utcnow().isoformat()
    observation_buffer.append(obs)
    await manager.broadcast(obs.dict()) #safe broadcast 
    ##################################################
    ## Next step: Tag connections with patient ID ####
    ##            Send only Ward A residents      ####

    return {"status": "streamed"}

@app.websocket("/ws/observation")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)

    try:
        while True:
            await websocket.receive_text()
    except Exception:
        await manager.disconnect(websocket)

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
def get_environment():
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
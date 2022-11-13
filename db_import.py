from challenge_api import crud, models, schemas
import json
from sqlalchemy.orm import Session
from challenge_api.database import session, engine
from datetime import datetime

'''
script to import data from planning.json to planning.db
'''

models.Base.metadata.create_all(bind=engine)
db = session()

with open('planning.json', 'r') as file:
    data = json.load(file)
    for elem in data:
        required_skills = []
        for skill in elem["requiredSkills"]:
            required_skills.append(crud.create_skill(
                db, schemas.SkillCreate(**skill)).name)
        optional_skills = []
        for skill in elem["optionalSkills"]:
            optional_skills.append(crud.create_skill(
                db, schemas.SkillCreate(**skill)).name)
        talent = crud.create_talent(db, schemas.TalentCreate(
            **{"id": elem["talentId"], "name": elem["talentName"], "grade": elem["talentGrade"]}))
        client = crud.create_client(db, schemas.ClientCreate(
            **{"id": elem["clientId"], "name": elem["clientName"], "industry": elem["industry"]}))
        manager = crud.create_manager(db, schemas.ManagerCreate(
            **{"id": elem["jobManagerId"], "name": elem["jobManagerName"]}))
        start_date = datetime.strptime(elem["startDate"], '%m/%d/%Y %I:%M %p')
        end_date = datetime.strptime(elem["endDate"], '%m/%d/%Y %I:%M %p')
        job = crud.create_job(db, schemas.JobCreate(**{"id": int(elem["id"]), "original_id": elem["originalId"], "booking_grade": elem["bookingGrade"], "operating_unit": elem["operatingUnit"], "office_city": elem["officeCity"], "office_postal_code": elem["officePostalCode"], "total_hours": float(
            elem["totalHours"]), "start_date": start_date, "end_date": end_date, "talent_id": talent.id, "manager_id": manager.id, "client_id": client.id, "required_skills": required_skills, "optional_skills": optional_skills}))
        print("Importing record number:",job.id)

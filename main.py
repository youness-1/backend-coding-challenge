from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import session, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

'''
API for data retrieval from planning.db with one example of each:
    #offset pagination
    #filtering
    #sorting
'''

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


@app.get("/jobs/pagination", response_model=List[schemas.Job]) #Offset Pagination
def read_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if skip < 0 or limit < 1:
        raise HTTPException(status_code=400, detail="Bad request")
    jobs = crud.get_jobs(db, skip=skip, limit=limit)
    return jobs


@app.get("/jobs/filtering", response_model=List[schemas.Job])
def read_job(id: int = None, original_id: str = None, operating_unit: str = None, client_id: str = None, office_city: str = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if skip < 0 or limit < 1:
        raise HTTPException(status_code=400, detail="Bad request")

    filters = schemas.JobFilter(id=id, original_id=original_id, operating_unit=operating_unit, client_id=client_id, office_city=office_city)
    db_jobs = crud.get_filter_job(db, filters, skip=skip, limit=limit)
    if db_jobs is None:
        raise HTTPException(status_code=404, detail="Jobs not found")
    return db_jobs

@app.get("/jobs/sorting", response_model=List[schemas.Job])
def get_sort_job(client_id: str, start_date: schemas.OrderEnum = None, end_date: schemas.OrderEnum = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if skip < 0 or limit < 1:
        raise HTTPException(status_code=400, detail="Bad request")
    sort= schemas.JobSort(client_id=client_id, start_date=start_date, end_date=end_date)
    db_jobs = crud.get_sort_job(db, sort, skip, limit)
    if db_jobs is None:
        raise HTTPException(status_code=404, detail="Jobs not found")
    return db_jobs
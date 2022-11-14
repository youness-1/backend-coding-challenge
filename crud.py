from sqlalchemy.orm import Session
from . import models, schemas
from sqlalchemy import desc

'''
Functions to read and write data from/into the database
'''


def get_job(db: Session, id: int):
    return db.query(models.Job).filter(models.Job.id == id).first()


def get_job_by_original_id(db: Session, id: str):
    return db.query(models.Job).filter(models.Job.original_id == id).first()


def get_jobs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Job).offset(skip).limit(limit).all()


def create_job(db: Session, job: schemas.JobCreate):
    db_job = get_job(db, id=job.id)
    if db_job is None:
        db_talent = get_talent(db, job.talent_id)
        if db_talent and db_talent is None:
            return None
        db_manager = get_manager(db, job.manager_id)
        if db_manager and db_manager is None:
            return None
        db_client = get_client(db, job.client_id)
        if db_client is None:
            return None
        db_required_skills = []
        for required_skill in job.required_skills:
            db_required_skill = get_skill(db, required_skill)
            if db_required_skill is None:
                return None
            db_required_skills.append(db_required_skill)
        db_optional_skills = []
        for optional_skill in job.optional_skills:
            db_optional_skill = get_skill(db, optional_skill)
            if db_optional_skill is None:
                return None
            db_optional_skills.append(db_optional_skill)

        job_params = vars(job)
        del job_params["client_id"]
        job_params["client"] = db_client
        del job_params["manager_id"]
        job_params["manager"] = db_manager
        del job_params["talent_id"]
        job_params["talent"] = db_talent
        del job_params["required_skills"]
        job_params["required_skills"] = db_required_skills
        del job_params["optional_skills"]
        job_params["optional_skills"] = db_optional_skills

        db_job = models.Job(**job_params)
        db.add(db_job)
        db.commit()
        db.refresh(db_job)
    return db_job


def get_talent(db: Session, id: str):
    return db.query(models.Talent).filter(models.Talent.id == id).first()


def get_talents(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Talent).offset(skip).limit(limit).all()


def create_talent(db: Session, talent: schemas.TalentCreate):
    db_talent = get_talent(db, talent.id)
    if db_talent is None:
        db_talent = models.Talent(**vars(talent))
        db.add(db_talent)
        db.commit()
        db.refresh(db_talent)
    return db_talent


def add_talent_to_job(db: Session, talent_id: str, job_id: int):
    job = get_job(db, job_id)
    if job is None:
        return None

    talent = get_talent(db, talent_id)
    if talent is None:
        return None

    job.talent = talent
    db.commit()
    return job


def get_client(db: Session, id: str):
    return db.query(models.Client).filter(models.Client.id == id).first()


def get_clients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Client).offset(skip).limit(limit).all()


def create_client(db: Session, client: schemas.ClientCreate):
    db_client = get_client(db, client.id)
    if db_client is None:
        db_client = models.Client(**vars(client))
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
    return db_client


def get_manager(db: Session, id: str):
    return get_talent(db, id)


def get_managers(db: Session, skip: int = 0, limit: int = 100):
    return get_talents(db, skip, limit)


def create_manager(db: Session, manager: schemas.ManagerCreate):
    db_manager = get_manager(db, manager.id)
    if db_manager is None:
        db_manager = models.Talent(**vars(manager))
        db.add(db_manager)
        db.commit()
    return db_manager


def get_skill(db: Session, name: str):
    return db.query(models.Skill).filter(models.Skill.name == name).first()


def get_skills(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Skill).offset(skip).limit(limit).all()


def create_skill(db: Session, skill: schemas.SkillCreate):
    db_skill = get_skill(db, name=skill.name)
    if db_skill is None:
        db_skill = models.Skill(**vars(skill))
        db.add(db_skill)
        db.commit()
        db.refresh(db_skill)
    return db_skill


def get_sort_job(db: Session, sort: schemas.JobSort, skip: int = 0, limit: int = 100):
    if sort.client_id:
        if sort.start_date == schemas.OrderEnum.ascending:
            return db.query(models.Job).filter(models.Job.client_id == sort.client_id).order_by(models.Job.start_date).offset(skip).limit(limit).all()
        elif sort.start_date == schemas.OrderEnum.descending:
            return db.query(models.Job).filter(models.Job.client_id == sort.client_id).order_by(models.Job.start_date.desc()).offset(skip).limit(limit).all()
        elif sort.end_date == schemas.OrderEnum.ascending:
            return db.query(models.Job).filter(models.Job.client_id == sort.client_id).order_by(models.Job.end_date).offset(skip).limit(limit).all()
        elif sort.end_date == schemas.OrderEnum.descending:
            return db.query(models.Job).filter(models.Job.client_id == sort.client_id).order_by(models.Job.end_date.desc()).offset(skip).limit(limit).all()
    return None

def get_filter_job(db, filters: schemas.JobFilter, skip: int = 0, limit: int = 100):
    filters=vars(filters)
    jobs = db.query(models.Job)
    for filter in filters:
        if filters[filter] is not None:
            jobs=jobs.filter(getattr(models.Job, filter) == filters[filter])
    return jobs.offset(skip).limit(limit).all()

def is_job_unassigned(db, job_id):
    job = get_job(db, job_id)
    if job is None:
        return None
    if job.talent_id:
        return True
    else:
        return False



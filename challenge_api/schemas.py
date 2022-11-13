from pydantic import BaseModel
from datetime import datetime
from enum import Enum, IntEnum

'''
Base classes are defined for common attributes
Create classes are defined for creating data
The rest are defined for reading/returning data from the API
'''


class TalentBase(BaseModel):
    id: str
    name: str
    grade: str | None = None


class TalentCreate(TalentBase):
    pass


class Talent(TalentBase):
    class Config:
        orm_mode = True


class ManagerBase(BaseModel):
    id: str
    name: str


class ManagerCreate(ManagerBase):
    pass


class Manager(TalentBase):
    class Config:
        orm_mode = True


class ClientBase(BaseModel):
    id: str
    name: str
    industry: str


class ClientCreate(ClientBase):
    pass


class Client(ClientBase):
    class Config:
        orm_mode = True


class SkillBase(BaseModel):
    name: str
    category: str


class SkillCreate(SkillBase):
    pass


class Skill(SkillBase):
    class Config:
        orm_mode = True


class JobBase(BaseModel):
    id: int
    original_id: str
    booking_grade: str | None = None
    operating_unit: str
    office_city: str | None = None
    office_postal_code: str 
    total_hours: float
    start_date: datetime
    end_date: datetime


class JobCreate(JobBase):
    talent_id: str
    manager_id: str
    client_id: str
    required_skills: list[str]
    optional_skills: list[str] | None = None
    pass


class Job(JobBase):
    talent: Talent | None = None
    manager: Manager
    client: Client
    required_skills: list[Skill] = []
    optional_skills: list[Skill] = []
    #is_unassigned: bool 
    class Config:
        orm_mode = True

class OrderEnum(str, Enum):
    ascending = 'asc'
    descending = 'desc'

class JobSort(BaseModel):
    client_id: str 
    start_date: OrderEnum | None = None
    end_date: OrderEnum | None = None

class JobFilter(BaseModel):
    id : int = None
    original_id: str | None = None
    operating_unit: str  | None = None
    client_id: str | None = None
    office_city: str | None = None

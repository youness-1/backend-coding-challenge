from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float, Table
from sqlalchemy.orm import relationship, backref
from .database import Base

'''
definition of SQLAlchemy models (classes and instances that interact with the database)
'''

required_job_skill = Table(
    "required_job_skill",
    Base.metadata,
    Column("job_id", Integer, ForeignKey("job.id")),
    Column("skill", String, ForeignKey("skill.name")),
)

optional_job_skill = Table(
    "optional_job_skill",
    Base.metadata,
    Column("job_id", Integer, ForeignKey("job.id")),
    Column("skill", String, ForeignKey("skill.name")),
)

class Job(Base):
    __tablename__ = 'job'
    id = Column(Integer, primary_key=True)
    original_id = Column(String, unique=True, nullable=False)
    talent_id = Column(String, ForeignKey("talent.id"))
    talent = relationship("Talent", foreign_keys=[talent_id])
    booking_grade = Column(String)
    operating_unit = Column(String, nullable=False)
    office_city = Column(String)
    office_postal_code = Column(String, nullable=False)
    manager_id = Column(String, ForeignKey("talent.id"))
    manager = relationship("Talent", foreign_keys=[manager_id])
    total_hours = Column(Float, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    client_id = Column(String, ForeignKey("client.id"), nullable=False)
    required_skills = relationship(
        "Skill", secondary=required_job_skill, back_populates="required_in_jobs"
    )
    optional_skills = relationship(
        "Skill", secondary=optional_job_skill, back_populates="optional_in_jobs"
    )


class Talent(Base):
    __tablename__ = 'talent'
    id = Column(String, primary_key=True)
    name = Column(String)
    grade = Column(String, nullable=True)


class Client(Base):
    __tablename__ = 'client'
    id = Column(String, primary_key=True)
    name = Column(String)
    industry = Column(String)
    jobs = relationship("Job", backref=backref("client"))


class Skill(Base):
    __tablename__ = 'skill'
    name = Column(String, primary_key=True)
    category = Column(String)
    required_in_jobs = relationship(
        "Job", secondary=required_job_skill, back_populates="required_skills"
    )
    optional_in_jobs = relationship(
        "Job", secondary=optional_job_skill, back_populates="optional_skills"
    )



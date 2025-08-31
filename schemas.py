from pydantic import BaseModel
from typing import List, Optional

class SkillBase(BaseModel):
    name: str
    level: Optional[str] = None

class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    link: Optional[str] = None

class ProfileBase(BaseModel):
    name: str
    email: str
    education: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None

class ProfileCreate(ProfileBase):
    skills: List[SkillBase] = []
    projects: List[ProjectBase] = []

class Skill(SkillBase):
    id: int
    class Config:
        orm_mode = True

class Project(ProjectBase):
    id: int
    class Config:
        orm_mode = True

class Profile(ProfileBase):
    id: int
    skills: List[Skill] = []
    projects: List[Project] = []
    class Config:
        orm_mode = True

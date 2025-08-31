import sys, os
sys.path.append(os.path.abspath(".")) 

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    education = Column(String(255))
    linkedin = Column(String(255))
    github = Column(String(255))

    skills = relationship("Skill", back_populates="profile", cascade="all, delete")
    projects = relationship("Project", back_populates="profile", cascade="all, delete")


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    level = Column(String(50))
    profile_id = Column(Integer, ForeignKey("profiles.id"))

    profile = relationship("Profile", back_populates="skills")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(150), nullable=False)
    description = Column(Text)
    link = Column(String(255))
    profile_id = Column(Integer, ForeignKey("profiles.id"))

    profile = relationship("Profile", back_populates="projects")

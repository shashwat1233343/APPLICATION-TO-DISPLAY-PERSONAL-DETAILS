from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from backend import models, schemas
from backend.database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in prod, restrict to frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/profiles/", response_model=schemas.Profile)
def create_profile(profile: schemas.ProfileCreate, db: Session = Depends(get_db)):
    db_profile = models.Profile(**profile.dict(exclude={"skills", "projects"}))
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)

    for skill in profile.skills:
        db_skill = models.Skill(**skill.dict(), profile_id=db_profile.id)
        db.add(db_skill)
    for project in profile.projects:
        db_project = models.Project(**project.dict(), profile_id=db_profile.id)
        db.add(db_project)

    db.commit()
    db.refresh(db_profile)
    return db_profile

@app.get("/profiles/{profile_id}", response_model=schemas.Profile)
def read_profile(profile_id: int, db: Session = Depends(get_db)):
    profile = db.query(models.Profile).filter(models.Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@app.get("/skills/top", response_model=list[schemas.Skill])
def top_skills(db: Session = Depends(get_db)):
    return db.query(models.Skill).limit(5).all()

@app.get("/projects/", response_model=list[schemas.Project])
def search_projects(skill: str, db: Session = Depends(get_db)):
    return db.query(models.Project).join(models.Profile).join(models.Skill).filter(models.Skill.name.ilike(f"%{skill}%")).all()

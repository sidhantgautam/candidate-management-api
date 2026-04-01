from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import List, Optional

# Define allowed status values using Enum
class CandidateStatus(str, Enum):
    """
    Enum for candidate status values
    """
    APPLIED = "applied"
    INTERVIEW = "interview"
    SELECTED = "selected"
    REJECTED = "rejected"

# Pydantic model for creating a new candidate
class CandidateCreate(BaseModel):
    name: str
    email: EmailStr
    skill: str
    status: CandidateStatus

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john@example.com",
                "skill": "Python",
                "status": "applied"
            }
        }

# Pydantic model for candidate with ID
class Candidate(CandidateCreate):
    """
    Complete candidate model including ID
    Inherits all fields from CandidateCreate and adds an ID
    """
    id: int
    name: str
    email: EmailStr
    skill: str
    status: CandidateStatus

# Pydantic model for updating candidate status
class CandidateStatusUpdate(BaseModel):
    """
    Model for updating only the status field of a candidate
    """
    status: CandidateStatus

# Initialize FastAPI application
app = FastAPI(
    title="Candidate Management API",
    description="API to manage recruitment candidates",
    version="1.0.0"
)

# In-memory storage
candidates: List[Candidate] = []
id_counter = 1

# Root endpoint - Health check
@app.get("/")
def read_root():
    """
    Root endpoint to verify the API is running
    """
    return {"message": "Candidate Management API is running"}

# Create a new candidate
@app.post("/candidates", response_model=Candidate, tags=["Candidates"])
def create_candidate(candidate_data: CandidateCreate):
    """
    Create a new candidate
    - Assigns a unique ID
    - Stores candidate in memory
    - Returns the created candidate
    """
    global id_counter
    
    # Create candidate with unique ID
    new_candidate = Candidate(
        id=id_counter,
        name=candidate_data.name,
        email=candidate_data.email,
        skill=candidate_data.skill,
        status=candidate_data.status
    )
    
    # Store candidate and increment counter
    candidates.append(new_candidate)
    id_counter += 1
    
    return new_candidate

# Get all candidates with optional status filter
@app.get("/candidates", response_model=List[Candidate], tags=["Candidates"])
def get_candidates(status: Optional[CandidateStatus] = None):
    """
    Get all candidates or filter by status
    - If status is provided: returns only candidates with that status
    - If status is not provided: returns all candidates
    """
    if status:
        # Filter candidates by status
        filtered_candidates = [c for c in candidates if c.status == status]
        return filtered_candidates
    
    # Return all candidates
    return candidates

# Update candidate status
@app.put("/candidates/{candidate_id}/status", response_model=Candidate, tags=["Candidates"])
def update_candidate_status(candidate_id: int, status_update: CandidateStatusUpdate):
    """
    Update the status of a specific candidate
    - Finds candidate by ID
    - Updates only the status field
    - Returns the updated candidate
    - Raises 404 if candidate not found
    """
    # Find candidate by ID
    for candidate in candidates:
        if candidate.id == candidate_id:
            # Update status
            candidate.status = status_update.status
            return candidate
    
    # Candidate not found
    raise HTTPException(
        status_code=404,
        detail=f"Candidate with id {candidate_id} not found"
    )

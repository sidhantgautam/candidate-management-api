# Candidate Management API

A backend API built using FastAPI to manage candidates in a recruitment system.

## Features

- Create a new candidate
- Get all candidates
- Filter candidates by status
- Update candidate status
- Input validation using Pydantic (email + enum)

## Tech Stack

- Python
- FastAPI
- Pydantic
- Uvicorn

## Project Setup

Follow these steps to set up and run the project:

1. Clone the repository:
```bash
git clone https://github.com/sidhantgautam/candidate-management-api.git
```

2. Navigate to the project folder:
```bash
cd candidate-management-api
```

3. Create a virtual environment (Recommended):

### macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

**Note:** You can skip creating a virtual environment and install dependencies globally, but it is not recommended.

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

## API Endpoints

### Create a New Candidate

**POST** `/candidates`

Request body:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "skill": "Python",
  "status": "applied"
}
```

### Get All Candidates

**GET** `/candidates`

### Get Candidates by Status

**GET** `/candidates?status=interview`

Available status values: `applied`, `interview`, `selected`, `rejected`

### Update Candidate Status

**PUT** `/candidates/{candidate_id}/status`

Request body:
```json
{
  "status": "interview"
}
```

## Testing

You can test the API using:

- **Swagger UI**: Navigate to `http://127.0.0.1:8000/docs` for interactive API documentation
- **Postman**: Import the endpoints and test manually

## Notes

- Data is stored in-memory (not persistent)
- Restarting the server resets all data
- Email validation is enforced automatically
- Status values are restricted to predefined enum values

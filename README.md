# SoonForward

A simple email waitlist signup app built with Flask and PostgreSQL. Users can submit their email to join the waitlist, with duplicate detection and basic validation.

## Setup

### 1. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Set up PostgreSQL

Create the database and table:

```sql
CREATE DATABASE soonforward;

\c soonforward

CREATE TABLE emails (
    email_address VARCHAR(250) UNIQUE NOT NULL
);
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```
DATABASE_URL=postgresql://localhost/soonforward
SECRET_KEY=your-secret-key
```

### 4. Run the app

```bash
python app.py
```

The app will be available at `http://localhost:5001`.

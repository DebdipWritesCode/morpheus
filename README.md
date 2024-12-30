# Form Builder

## Description

Form Builder is a web application that allows users to create forms, manage submissions, and view analytics on responses. Built with Django on the backend and React with TypeScript on the frontend, the application is designed to provide a seamless experience for form creation and management. The project uses PostgreSQL as the database and Docker for easy setup.

## Tech Stack

- **Backend:** Django, Python
- **Frontend:** React, TypeScript
- **Database:** PostgreSQL (with Docker)
- **Deployment:** Docker (for PostgreSQL), Makefile (for task automation)

## Setup Instructions

Follow the steps below to set up the project on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/DebdipWritesCode/morpheus.git
cd morpheus
```

### 2. Set Up Environment Variables

Create a `.env` file at the root of your project (where the `README.md` file is located) with the following content:

```bash
DB_NAME=form_builder
DB_USER="your_name"
DB_PASSWORD="your_password"
DB_HOST=127.0.0.1
DB_PORT=5431
SECRET_KEY="xyz"
DEBUG=True
```

### 3. Set Up Docker and Database

Run the following commands to set up the PostgreSQL database using Docker:

```bash
make postgres
make created
```

### 4. Backend Setup

Now, move into the `Backend` directory:

```bash
cd Backend
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate  # For Windows
```

Install the backend dependencies:

```bash
pip install -r requirements.txt
```

Go back to the root directory:

```bash
cd ..
```

Run database migrations and start the backend server:

```bash
make makemigrations
make migrateup
make back_server
```

The backend server will be running on port `8000`.

### 5. Frontend Setup

Go to the `Frontend` directory:

```bash
cd Frontend
```

Create a `.env` file in the `Frontend` directory and add the following environment variable:

```bash
VITE_BACKEND_URL=http://localhost:8000
```

Install frontend dependencies:

```bash
npm install
```

Start the frontend server:

```bash
npm run dev
```

The frontend will be running on port `5173`.

## Usage Guide

### Postman Collection

We have included a Postman collection in the `Backend` directory that contains all the available API routes. You can use it to test the endpoints with sample data.

### API Routes

Below is a list of the available routes and how to use them:

#### `POST /auth/signup`

- **Description:** Allows a new user to sign up.
- **Request Body:**
  ```json
  {
    "username": "testuser",
    "password": "testpassword"
  }
  ```

#### `POST /auth/login`

- **Description:** Allows an existing user to log in.
- **Request Body:**
  ```json
  {
    "username": "testuser",
    "password": "testpassword"
  }
  ```

#### `POST /create-form`

- **Description:** Allows the creation of a new form with questions.
- **Request Body:**
  ```json
  {
    "form_name": "Survey 1",
    "questions": [
      { "question_text": "What is your favorite color?" },
      { "question_text": "How old are you?" }
    ]
  }
  ```

#### `GET /get-forms`

- **Description:** Retrieves all the forms created.
- **Response:**
  ```json
  [
    {
      "id": 1,
      "form_name": "Survey 1"
    },
    {
      "id": 2,
      "form_name": "Survey 2"
    }
  ]
  ```

#### `GET /get-form/<form_id>`

- **Description:** Retrieves a specific form by ID.
- **URL Parameter:** `form_id` (e.g., `/get-form/1`).

#### `POST /submit-response`

- **Description:** Submits responses to a form.
- **Request Body:**
  ```json
  {
    "form_id": 1,
    "responses": [
      { "question_id": 1, "answer": "Blue" },
      { "question_id": 2, "answer": "25" }
    ]
  }
  ```

#### `GET /show-analytics/<form_id>`

- **Description:** Retrieves analytics for a specific form.
- **URL Parameter:** `form_id` (e.g., `/show-analytics/1`).
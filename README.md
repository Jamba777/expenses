# Expense Tracker API

This is a Django-based API for managing users and their expenses. The API supports CRUD operations for users and expenses, filtering expenses by date range, and summarizing expenses by category.

## Features
- **User Management:** Create and list users.
- **Expense Management:** Create, retrieve, update, and delete expenses.
- **Filter by Date Range:** Retrieve expenses for a user within a specified date range.
- **Category Summary:** Summarize total expenses per category for a given user and month.

## Stack used
- **Django:** Backend framework.
- **Django REST Framework (DRF):** For API development.
- **PostgreSQL:** Database.
- **Docker & Docker Compose:** For containerized deployment.

## Setup Instructions

### Prerequisites
- Install [Docker](https://www.docker.com/ "Docker").
- Install [Docker Compose](https://docs.docker.com/compose/install/ "Docker Compose").

### 1. Clone the Repository
```bash
git clone https://github.com/Jamba777/expenses.git
cd expense-tracker
```

### 2. Running the Application
Run the following command to build the Docker images and start the containers:
```bash
docker-compose up --build
```
This will:

1. Build the Django app container.
2. Set up the PostgreSQL database container.
3. Run the API server on http://localhost:8000.

### 3. Access the Application
- **API Endpoints:** http://localhost:8000/api/
- **Swagger UI:** http://localhost:8000/api/swagger/

### Stopping the Application
```bash
docker-compose down
```

### Rebuilding the Application
```bash
docker-compose up --build
```
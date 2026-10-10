# Student Information System

A command-line Student Information System built in Python with JSON storage,
modular architecture, configuration management, and logging.

## Features
- Add, view, update and delete student records (CRUD)
- JSON data persistence
- Input validation (name, email, course, year level)
- Logging to console and `logs/app.log`
- Unit tests

## Project Structure
```
student-info-system/
├── src/
│   ├── models/student.py
│   ├── services/student_service.py
│   ├── utils/config.py, validators.py
│   └── main.py
├── data/          # students.json 
├── config/config.json
├── logs/
├── tests/
├── README.md
├── requirements.txt
└── .gitignore
```

## Setup & Run
```bash
git clone https://github.com/<your-username>/student-info-system.git
cd student-info-system
python src/main.py
```
Requires Python 3.8+. No external dependencies.

## Configuration
Edit `config/config.json` to change the data file, log file or log level.

## Run Tests
```bash
python -m unittest discover tests
```

## Git Workflow
Feature branches are merged into `main` via pull requests
(e.g. `feature/add-student`, `feature/update-delete`).

## Author
<Euburn Ken M. De Asis>

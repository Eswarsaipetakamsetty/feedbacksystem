# 🌟 Django Feedback System

A role-based feedback platform where employees can submit self-feedback, and managers can review, comment, assign scores, and manage teams effectively — just like modern ERP systems.

---

## 🚀 Features

### 🔐 Authentication
- Login/Signup with email/password
- JWT-based user authentication
- View profile by email

### 🧑‍💼 Role-Based Access
- **Employees** can:
  - Submit feedback to themselves
  - Accept team invitations
  - View feedback and comments
- **Managers** can:
  - Create teams by employee emails
  - Review submitted feedback
  - Add comments and scores
  - View all feedback and team stats

### 💬 Feedback System
- Self-feedback creation
- Manager review with score, comments
- Activity tracking on actions

### 👥 Team Management
- Create teams with member emails
- Accept invitations
- Add members (manager-only)
- List teams, get stats like accepted members

### 📊 Analytics
- Count of:
  - Feedbacks submitted
  - Reviewed feedbacks
  - Team members accepted
  - Total teams per user

### 📦 Activity Tracker
- Log activities like team creation, feedback submission, review

---

## 🛠 Tech Stack

- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL
- **Auth**: JWT
- **Containerization**: Docker, Docker Compose
- **Frontend**: React + TypeScript (with Profile page and API hooks)

---

## 📂 Project Structure

<pre> ``` feedbacksystem/ ├── activity/ ├── feedback/ ├── team/ ├── userauth/ ├── feedbacksystem/ # Main Django project ├── manage.py ├── Dockerfile ├── docker-compose.yml ├── requirements.txt ``` </pre>

---

## 🐳 Running with Docker

### 1. Clone the repo

```bash
git clone <https://github.com/Eswarsaipetakamsetty/feedbacksystem>
cd feedbacksystem

```

### 2. create a .env file

```bash
POSTGRES_DB=mydb
POSTGRES_USER=user
POSTGRES_PASSWORD=password

```
Or skip this step and use default values already set in docker-compose.yml.

###3. Run the docker container
```bash
docker-compose up --build
```

### 4. Run Migrations (If Needed Manually)

```bash

docker-compose exec django-app python manage.py makemigrations
docker-compose exec django-app python manage.py migrate

```

### 🔑 API Endpoints
### 🔐 Auth

| Method | Endpoint                                     | Description                 |
| ------ | -------------------------------------------- | --------------------------- |
| POST   | `/auth/register/`                            | Register a new user         |
| POST   | `/auth/login/`                               | Login and receive JWT token |
| GET    | `/auth/user/by_email/?email=xyz@example.com` | Get user by email           |
| GET    | `/auth/user/<id>/`                           | Get user by ID              |

### 👤 Profile

| Method | Endpoint                                      | Description             |
| ------ | --------------------------------------------- | ----------------------- |
| GET    | `/auth/user/by_email/?email=user@example.com` | View any user’s profile |

### 👥 Teams

| Method | Endpoint                          | Description                              |
| ------ | --------------------------------- | ---------------------------------------- |
| POST   | `/team/create/`                   | Create team by email list (manager only) |
| PATCH  | `/team/add-members/<team_id>`     | Add team members (manager only)          |
| PATCH  | `/team/accept-invite/<team_id>/`  | Accept team invitation                   |
| GET    | `/team/viewteam/`                 | Get teams the user is part of            |
| GET    | `/team/count/`                    | Get total number of teams user is in     |
| GET    | `/team/manager_teams/`            | Count of accepted members in team        |

### 💬 Feedback

| Method | Endpoint                     | Description                                  |
| ------ | ---------------------------- | -------------------------------------------- |
| POST   | `/feedback/create/`          | Submit feedback                              |
| PATCH  | `/feedback/review/<id>/`     | Review feedback (manager only)               |
| GET    | `/feedback/view/employee/`   | Get self feedbacks                           |
| GET    | `/feedback/pending/count/`   | Get all unreviewed feedbacks                 |
| GET    | `/feedback/view/`            | Get feedbacks given by manager               |
| GET    | `/feedback/reviewed/`        | Get all reviewed feedbacks (by manager only) |
| GET    | `/feedback/count/`           | Get count of submitted feedbacks             |

### 💭 Comments

| Method | Endpoint                            | Description                |
| ------ | ----------------------------------- | -------------------------- |
| POST   | `/feedback/comment/`                | Add comment to feedback    |
| GET    | `/feedback/comments/<feedback_id>/` | Get comments on a feedback |

### 🔍 Environment Variables
Environment variables are set via Docker Compose or .env:
```bash
POSTGRES_DB=mydb
POSTGRES_USER=user
POSTGRES_PASSWORD=password
```

### Django settings.py Database Config:

```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'mydb'),
        'USER': os.environ.get('POSTGRES_USER', 'user'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'password'),
        'HOST': 'db',
        'PORT': '5432',
    }
}
```

### 🧪 Testing
Run tests inside the Docker container:

```bash
docker-compose exec django-app python manage.py test
```

### 🤝 Contributing
Pull requests are welcome. Please ensure your changes are well tested and linted.



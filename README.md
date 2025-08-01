# prag_system
# Django Project Setup

This guide helps you set up and run the Django project locally.

## Setup Instructions

```bash
# Clone the repository
git clone https://github.com/IndradevKr/prag_system.git
cd prag_system
```
# Create and activate virtual environment
# For Linux/macOS
```bash
python3 -m venv venv
source venv/bin/activate
```

# For Windows
```bash
python -m venv venv
venv\Scripts\activate
```

# Upgrade pip and install required packages
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

# Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

# Create superuser
```bash
python manage.py createsuperuser
```

# Run the development server
```bash
python manage.py runserver
```
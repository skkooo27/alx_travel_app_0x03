# ALX Travel App

This Django project is designed for managing travel listings with background task processing using Celery and RabbitMQ.

## Features

- Travel listing management
- Booking system
- Asynchronous email notifications for bookings using Celery
- REST API with Django REST Framework

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Variables
Create a `.env` file in the project root with the following variables:
```
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=3306
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_email_app_password
```

### 3. Database Setup
Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. RabbitMQ Setup
Install and start RabbitMQ:

**On Windows:**
```bash
# Install RabbitMQ using Chocolatey
choco install rabbitmq

# Or download from: https://www.rabbitmq.com/install-windows.html

# Start RabbitMQ service
rabbitmq-service start

# Enable management plugin (optional, for web UI)
rabbitmq-plugins enable rabbitmq_management
```

**On macOS:**
```bash
# Install using Homebrew
brew install rabbitmq

# Start RabbitMQ
brew services start rabbitmq

# Enable management plugin (optional)
rabbitmq-plugins enable rabbitmq_management
```

**On Linux:**
```bash
# Install RabbitMQ
sudo apt-get update
sudo apt-get install rabbitmq-server

# Start RabbitMQ
sudo systemctl start rabbitmq-server
sudo systemctl enable rabbitmq-server

# Enable management plugin (optional)
sudo rabbitmq-plugins enable rabbitmq_management
```

RabbitMQ Management UI will be available at: http://localhost:15672 (guest/guest)

### 5. Start Celery Worker
In a new terminal, start the Celery worker:
```bash
celery -A alx_travel_app worker --loglevel=info
```

### 6. Start Django Server
```bash
python manage.py runserver
```

## API Endpoints

- `GET/POST /api/listings/` - List and create listings
- `GET/POST /api/bookings/` - List and create bookings (triggers email notification)

## Testing Email Notifications

### 1. Create a Booking
Use the API to create a booking:
```bash
curl -X POST http://localhost:8000/api/bookings/ \
  -H "Content-Type: application/json" \
  -d '{
    "listing": 1,
    "guest_name": "John Doe",
    "check_in": "2024-12-01",
    "check_out": "2024-12-05"
  }'
```

### 2. Monitor Celery Worker
The Celery worker terminal should show the task being processed:
```
[2024-11-15 10:30:00,000: INFO/MainProcess] Received task: listings.tasks.send_booking_confirmation_email[uuid]
[2024-11-15 10:30:00,001: INFO/MainProcess] Task listings.tasks.send_booking_confirmation_email[uuid] succeeded: Email sent successfully to john.doe@example.com
```

### 3. Check Email
The booking confirmation email will be sent to: `john.doe@example.com`

## Project Structure

```
alx_travel_app/
├── alx_travel_app/
│   ├── __init__.py          # Celery app initialization
│   ├── celery.py            # Celery configuration
│   ├── settings.py          # Django settings with Celery config
│   ├── listings/
│   │   ├── models.py        # Listing and Booking models
│   │   ├── views.py         # API views with async email trigger
│   │   ├── tasks.py         # Celery tasks for email notifications
│   │   └── serializers.py   # DRF serializers
│   └── ...
├── requirements.txt         # Python dependencies
└── README.md
```

## Background Tasks

The application uses Celery with RabbitMQ to handle background tasks:

- **Email Notifications**: When a booking is created, an email confirmation is sent asynchronously
- **Task Queue**: RabbitMQ serves as the message broker
- **Worker Process**: Celery worker processes background tasks

## Troubleshooting

### RabbitMQ Issues
- Ensure RabbitMQ service is running
- Check if port 5672 is available
- Verify connection: `telnet localhost 5672`

### Celery Issues
- Make sure Django settings are properly configured
- Check Celery worker logs for errors
- Ensure all dependencies are installed

### Email Issues
- Configure email credentials in `.env` file
- For Gmail, use App Passwords instead of regular password
- Check spam folder for test emails

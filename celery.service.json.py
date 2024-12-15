[Unit]
Description=Celery Service
After=network.target

[Service]
User=your_user
WorkingDirectory=/path/to/budget_app
ExecStart=/path/to/venv/bin/celery -A app.celery worker --loglevel=info

[Install]
WantedBy=multi-user.target
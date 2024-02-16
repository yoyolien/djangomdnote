echo "Collect static files"
python manage.py collectstatic --noinput

# Make migrations
echo "Make migrations"
python manage.py makemigrations

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

gunicorn djangonote.wsgi:application --bind 0.0.0.0:8000
exec "$@"
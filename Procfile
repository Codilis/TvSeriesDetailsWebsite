web: gunicorn TvSeriesDetails.wsgi:application --preload -b 0.0.0.0:5000
python manage.py collectstatic --noinput
manage.py migrate

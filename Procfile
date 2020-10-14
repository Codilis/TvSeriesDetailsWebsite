web: gunicorn TvSeriesDetails.wsgi:application --log-file - --log-level debug
scheduler: python scheduler.py
python manage.py collectstatic --noinput
manage.py migrate

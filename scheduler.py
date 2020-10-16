from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import traceback
import pytz
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TvSeriesDetails.settings")
import django
django.setup()
from django.core.management import settings
from main.models import UserTvSeries, UserTvSeriesModel, TvSeriesDetailsModel
from main.imdb_functions import get_tv_series_name, get_series_latest_info, tv_series_email
from django.conf import settings
from django.core.mail import EmailMessage
sched = BlockingScheduler()


# @sched.scheduled_job('interval', minutes=1)
@sched.scheduled_job('cron', day_of_week='mon-sun', hour=7)
def scheduled_job():
	# print('This job is run every day at 7pm.')
		tv_series_list = TvSeriesDetailsModel.objects.all()
		for series in tv_series_list:
			try:
				series_id = series.tv_series_id
				tv_series_name = series.tv_series_name
				email_subject, email_body = get_series_latest_info(series_id)
				changed = False
				if email_body != series.email_body:
					series.email_body = email_body
					series.email_subject = email_subject
					series.save()
					changed = True

				# Send Email if time is now
				recipient_list = []
				user_with_series = UserTvSeriesModel.objects.filter(tv_series_id=series_id)
				now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=pytz.UTC)
				email_send_days = {"N":now-timedelta(days=10000), "M":now-relativedelta(months=1),
									"D":now, "W":now-timedelta(days=7), "H":now-relativedelta(months=6),
									"Y":now-relativedelta(years=1), "S":now-timedelta(days=10000)}
				for user in user_with_series:
					last_email_sent = user.last_email_sent.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=pytz.UTC)
					if changed and user.update_type == "S":
						recipient_list.append(user.user)
						user.last_email_sent = (datetime.utcnow()+timedelta(hours=5, minutes=30))
					elif last_email_sent < email_send_days[user.update_type]:
						recipient_list.append(user.user)
						user.last_email_sent = (datetime.utcnow()+timedelta(hours=5, minutes=30))
				if recipient_list:
					email_from = settings.EMAIL_HOST_USER
					EmailMessage(email_subject, email_body, email_from, bcc=recipient_list).send(fail_silently=True)
			except Exception as e:
				email_from = settings.EMAIL_HOST_USER
				email_to = [settings.ADMIN_EMAIL]
				subject = f"IMDb Error {datetime.now().strftime('%d-%m-%YT%H:%M:%S')}"
				body = traceback.format_exc()
				EmailMessage(subject, body, email_from, bcc=email_to).send(fail_silently=True)



sched.start()

from imdb import IMDb, IMDbError
import traceback
from datetime import datetime, timedelta
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

PATH = os.getcwd()
def get_tv_series_name(tv_series_id):
	if not tv_series_id.lower().startswith('tt'):
		return ('NOTTVSERIES', '')
	try:
		ia = IMDb()
		series  = ia.get_movie(tv_series_id[2:])
		print(series.data)
		print(series['seasons'])
	except Exception as e:
		return ('CONNECTIONERROR', '000000')
	try:
		if 'episode of' in series:
				series = series.data['episode of']
				return series['title'], series.getID()
		elif 'title' in series:
		        return series['title'], series.getID()
		return ('CONNECTIONERROR', '000000')
	except:
		f = open('{}\\error_logs.txt'.format(PATH), 'a+')
		f.close()
		with open('{}\\error_logs.txt'.format(PATH), 'r+') as f:
			lines = f.readlines()
			f.seek(0)
			f.write('[{}] {}\n'.format(datetime.strftime(datetime.utcnow()+timedelta(hours=5,minutes=30), "%d-%m-%YT%H:%M:%S"), traceback.format_exc()))
			f.writelines(lines)
		f.close()
		return ('NOTFOUNDSERIES', '000000')

def get_series_latest_info(tv_series_id):
	ia = IMDb()
	series  = ia.get_movie(tv_series_id[2:])
	total_season = series['seasons']
	for latest_season in range(1, total_season+1):
		series_url = 'https://www.imdb.com/title/{}/episodes?season={}'.format(tv_series_id, latest_season)
		series_webpage = urlopen(series_url)
		soup = BeautifulSoup(series_webpage, 'html.parser')
		regex = re.compile('.*list_item.*')
		season_episodes_info = soup.find('div', attrs={'class': 'list detail eplist'}).find_all('div', attrs={'class':regex})
		total_episodes = 0
		last_episode_number = 0
		for episode in season_episodes_info:
			total_episodes += 1
			episode_information = episode.find('div', attrs={'class':'info'})
			episode_number = int(episode_information.find('meta', attrs={'itemprop':'episodeNumber'})['content'])
			air_date = episode_information.find('div', attrs={'class':'airdate'}).text.strip()
			episode_name = episode_information.find('a', attrs={'itemprop':'name'}).text.strip()
			plot = episode_information.find('div', attrs={'class':'item_description'}).text.strip()
			if plot == 'Know what this is about?\n Be the first one to add a plot.':
				plot = 'Not Announced'
			if episode_number > last_episode_number and episode_name != f"Episode #{latest_season}.{episode_number}":
				latest_declared_name = episode_name
				latest_episode_number = episode_number
				release_date = air_date
				latest_plot = plot
				announcement_season = latest_season
				announced_season_total_episode = len(season_episodes_info)

	print("New Update For", tv_series_id)
	print("Season", announcement_season, "Announcements")
	print("total Episodes: {announced_season_total_episode},".format(announced_season_total_episode=announced_season_total_episode))
	print("Latest Episode Name: {latest_declared_name},".format(latest_declared_name=latest_declared_name))
	print("Latest Episode Number: {latest_episode_number},".format(latest_episode_number=latest_episode_number))
	print("Release Date: {release_date},".format(release_date=release_date))
	print("Plot: {latest_plot}".format(latest_plot=latest_plot))
	if announcement_season < total_season:
		print(",".join(map(str, range(announcement_season+1, total_season+1))), "are also Announced")

	"""
	Test Series: Upload, Stranger Things, THe Boys
	Email Subject: New Update For {Tv Series}
	Email Body: Season {latest_season} Announcement,
				total Episodes: {total_episodes},
				Latest Episode Name: {latest_declared_name},
				Latest Episode Number: {latest_episode_number},
				Release Date: {release_date},
				'Plot': {latest_plot}

	"""

# tv_series_id = 'tt2261227'
# get_series_latest_info(tv_series_id)

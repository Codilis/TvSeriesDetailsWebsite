try:
   from setuptools import setup, find_packages
except ImportError:
   from ez_setup import use_setuptools
   use_setuptools()
   from setuptools import setup, find_packages

setup(
   name='TvSeriesDetails',
   version='0.1',
   description='',
   author='Palash Jain',
   author_email='palash.j22@gmail.com',
   install_requires=[
      'django',
	  'Jinja2',
	  'python-environ',
	  'django-heroku',
	  'gunicorn',
	  'IMDbPY',
	  'beautifulsoup4',
	  'django-smtp-ssl'
   ],
   packages=find_packages(exclude=['ez_setup']),
   include_package_data=True,
)

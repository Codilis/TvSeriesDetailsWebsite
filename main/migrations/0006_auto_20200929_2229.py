# Generated by Django 3.1.1 on 2020-09-29 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20200929_2216'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserTvSeriesModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tv_series_id', models.CharField(max_length=1023)),
                ('update_type', models.CharField(max_length=1023)),
                ('date_added', models.DateTimeField()),
                ('user', models.CharField(max_length=1023)),
            ],
        ),
        migrations.DeleteModel(
            name='UserTvSeries',
        ),
    ]
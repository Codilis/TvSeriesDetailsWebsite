# Generated by Django 3.1.1 on 2020-09-28 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0003_delete_usertvseries'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserTvSeriesModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
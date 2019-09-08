# Generated by Django 2.2.3 on 2019-09-08 10:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BadgeAward',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('awarded_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('slug', models.CharField(max_length=255)),
                ('level', models.IntegerField()),
                ('points_at', models.IntegerField(default=0)),
                ('site', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='sites.Site', verbose_name='site')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='badges_earned', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

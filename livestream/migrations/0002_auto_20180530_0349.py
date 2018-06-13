# Generated by Django 2.0.5 on 2018-05-30 03:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('livestream', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rating', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='approvalrequest',
            name='appeal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='approval_requests', to='livestream.Appeal'),
        ),
        migrations.AddField(
            model_name='approvalrequest',
            name='helper',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appeal',
            name='helper',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='offers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appeal',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to=settings.AUTH_USER_MODEL),
        ),
    ]

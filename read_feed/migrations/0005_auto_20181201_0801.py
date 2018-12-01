# Generated by Django 2.1.3 on 2018-12-01 08:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('read_feed', '0004_auto_20181201_0757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='fbuser',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='read_feed.FBUser', verbose_name='Facebook User'),
        ),
        migrations.AlterField(
            model_name='postphoto',
            name='post',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='read_feed.Post', verbose_name='Post'),
            preserve_default=False,
        ),
    ]
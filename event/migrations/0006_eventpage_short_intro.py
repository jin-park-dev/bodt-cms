# Generated by Django 2.0.8 on 2018-09-25 06:48

from django.db import migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0005_auto_20180911_0615'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventpage',
            name='short_intro',
            field=wagtail.core.fields.RichTextField(blank=True),
        ),
    ]

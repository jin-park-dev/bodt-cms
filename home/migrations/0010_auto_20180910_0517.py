# Generated by Django 2.0.8 on 2018-09-10 05:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailforms', '0003_capitalizeverbose'),
        ('wagtailcore', '0040_page_draft_title'),
        ('wagtailredirects', '0006_redirect_increase_max_length'),
        ('home', '0009_auto_20180906_0612'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='showspage',
            name='page_ptr',
        ),
        migrations.DeleteModel(
            name='ShowsPage',
        ),
    ]

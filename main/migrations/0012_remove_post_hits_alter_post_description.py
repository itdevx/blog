# Generated by Django 4.0.3 on 2022-05-26 03:59

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_alter_post_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='hits',
        ),
        migrations.AlterField(
            model_name='post',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='متن مقاله'),
        ),
    ]

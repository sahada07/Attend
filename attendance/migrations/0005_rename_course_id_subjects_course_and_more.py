# Generated by Django 5.1.5 on 2025-02-17 11:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0004_rename_course_subjects_course_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subjects',
            old_name='course_id',
            new_name='course',
        ),
        migrations.RenameField(
            model_name='subjects',
            old_name='staff_id',
            new_name='staff',
        ),
    ]

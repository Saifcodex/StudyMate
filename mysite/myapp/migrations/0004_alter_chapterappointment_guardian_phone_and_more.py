# Generated by Django 5.1.6 on 2025-05-04 14:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_book_cartitem_order_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapterappointment',
            name='guardian_phone',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='chapterappointment',
            name='phone_number',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='generalappointment',
            name='guardian_phone',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='generalappointment',
            name='phone_number',
            field=models.IntegerField(),
        ),
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField()),
                ('tutor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.generaltutor')),
            ],
        ),
        migrations.AlterField(
            model_name='generalappointment',
            name='preferred_time',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.timeslot'),
        ),
        migrations.CreateModel(
            name='TimeSlot1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField()),
                ('tutor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.chaptertutor')),
            ],
        ),
        migrations.AlterField(
            model_name='chapterappointment',
            name='preferred_time',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.timeslot1'),
        ),
    ]

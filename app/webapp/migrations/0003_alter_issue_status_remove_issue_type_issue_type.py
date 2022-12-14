# Generated by Django 4.1.2 on 2022-10-07 11:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_alter_status_options_alter_issue_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issue', to='webapp.status', verbose_name='Status'),
        ),
        migrations.RemoveField(
            model_name='issue',
            name='type',
        ),
        migrations.AddField(
            model_name='issue',
            name='type',
            field=models.ManyToManyField(default='task', related_name='issue', to='webapp.type'),
        ),
    ]

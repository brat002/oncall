# Generated by Django 4.2.15 on 2025-01-20 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alerts', '0073_update_direct_paging_integration_non_default_routes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='escalationpolicy',
            name='step',
            field=models.IntegerField(choices=[(0, 'Wait'), (1, 'Notify User'), (2, 'Notify Whole Channel'), (3, 'Repeat Escalation (5 times max)'), (4, 'Resolve'), (5, 'Notify Group'), (6, 'Notify Schedule'), (7, 'Notify User (Important)'), (8, 'Notify Group (Important)'), (9, 'Notify Schedule (Important)'), (10, 'Trigger Outgoing Webhook'), (11, 'Notify User (next each time)'), (12, 'Continue escalation only if time is from'), (13, 'Notify multiple Users'), (14, 'Notify multiple Users (Important)'), (15, 'Continue escalation if >X alerts per Y minutes'), (16, 'Trigger Webhook'), (17, 'Notify all users in a Team'), (18, 'Notify all users in a Team (Important)'), (19, 'Declare Incident'), (20, 'Notify User (next each time) (Important)')], default=None, null=True),
        ),
    ]

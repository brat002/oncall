# Generated by Django 4.2.15 on 2024-10-17 19:19
import logging

from django.db import migrations
import django_migration_linter as linter

logger = logging.getLogger(__name__)


def populate_default_slack_channel(apps, schema_editor):
    Organization = apps.get_model("user_management", "Organization")
    SlackChannel = apps.get_model("slack", "SlackChannel")

    logger.info("Starting migration to populate default_slack_channel field.")

    # NOTE: the following raw SQL only works on mysql, fall back to the less-efficient (but working) ORM method
    # for non-mysql databases
    #
    # see the following references for more information:
    # https://github.com/grafana/oncall/issues/5244#issuecomment-2493688544
    # https://github.com/grafana/oncall/pull/5233/files#diff-e69e0d7ecf51300be2ca5f4239c5f08b4c6e41de9856788f85a522001595a192
    if schema_editor.connection.vendor == "mysql":
        sql = f"""
        UPDATE {Organization._meta.db_table} AS org
        JOIN {SlackChannel._meta.db_table} AS sc ON sc.slack_id = org.general_log_channel_id
                            AND sc.slack_team_identity_id = org.slack_team_identity_id
        SET org.default_slack_channel_id = sc.id
        WHERE org.general_log_channel_id IS NOT NULL
        AND org.slack_team_identity_id IS NOT NULL;
        """

        with schema_editor.connection.cursor() as cursor:
            cursor.execute(sql)
            updated_rows = cursor.rowcount  # Number of rows updated

        logger.info(f"Bulk updated {updated_rows} organizations with their default Slack channel.")
        logger.info("Finished migration to populate default_slack_channel field.")
    else:
        queryset = Organization.objects.filter(general_log_channel_id__isnull=False, slack_team_identity__isnull=False)
        total_orgs = queryset.count()
        updated_orgs = 0
        missing_channels = 0
        organizations_to_update = []

        logger.info(f"Total organizations to process: {total_orgs}")

        for org in queryset:
            slack_id = org.general_log_channel_id
            slack_team_identity = org.slack_team_identity

            try:
                slack_channel = SlackChannel.objects.get(slack_id=slack_id, slack_team_identity=slack_team_identity)

                org.default_slack_channel = slack_channel
                organizations_to_update.append(org)

                updated_orgs += 1
                logger.info(
                    f"Organization {org.id} updated with SlackChannel {slack_channel.id} (slack_id: {slack_id})."
                )
            except SlackChannel.DoesNotExist:
                missing_channels += 1
                logger.warning(
                    f"SlackChannel with slack_id {slack_id} and slack_team_identity {slack_team_identity} "
                    f"does not exist for Organization {org.id}."
                )

        if organizations_to_update:
            Organization.objects.bulk_update(organizations_to_update, ["default_slack_channel"])
            logger.info(f"Bulk updated {len(organizations_to_update)} organizations with their default Slack channel.")

        logger.info(
            f"Finished migration. Total organizations processed: {total_orgs}. "
            f"Organizations updated: {updated_orgs}. Missing SlackChannels: {missing_channels}."
        )


class Migration(migrations.Migration):

    dependencies = [
        ("user_management", "0025_organization_default_slack_channel"),
    ]

    operations = [
        # simply setting this new field is okay, we are not deleting the value of general_log_channel_id
        # therefore, no need to revert it
        linter.IgnoreMigration(),
        migrations.RunPython(populate_default_slack_channel, migrations.RunPython.noop),
    ]

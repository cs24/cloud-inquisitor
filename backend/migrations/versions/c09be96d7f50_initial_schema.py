"""Initial schema

Revision ID: c09be96d7f50
Revises: None
Create Date: 2017-08-15 11:52:03.227236

"""
import os
from collections import namedtuple

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c09be96d7f50'
down_revision = None


USE_PARTITIONING = os.environ.get('AUDIT_USE_PARTITIONS', 'true').lower() in ('true', 'yes', 'y')
Partition = namedtuple('Partition', ('table', 'partitions', 'key'))
partitions = [
    Partition('tags', os.environ.get('TAG_PARTITIONS', 20), 'tag_id'),
    Partition('resources', os.environ.get('RESOURCE_PARTITIONS', 8), 'resource_id'),
    Partition('resource_properties', os.environ.get('TAG_PARTITIONS', 20), 'resource_id'),
    Partition('issues', os.environ.get('ISSUE_PARTITIONS', 8), 'issue_id'),
    Partition('issue_properties', os.environ.get('ISSUE_PROP_PARTITIONS', 20), 'issue_id'),
    Partition('auditlog', os.environ.get('AUDIT_LOG_PARTITIONS', 20), 'audit_log_event_id'),
    Partition('logs', os.environ.get('LOG_PARTITIONS', 20), 'log_event_id'),
    Partition('emails', os.environ.get('EMAIL_PARTITIONS', 20), 'email_id')
]


def upgrade():
    op.create_table('accounts',
        sa.Column('account_id', mysql.INTEGER(), nullable=False, autoincrement=True),
        sa.Column('account_name', sa.String(length=64), nullable=False),
        sa.Column('account_number', sa.String(length=12), nullable=False),
        sa.Column('contacts', mysql.JSON(), nullable=False),
        sa.Column('ad_group_base', sa.String(length=64), nullable=True),
        sa.Column('enabled', sa.SmallInteger(), nullable=False),
        sa.Column('required_roles', mysql.JSON(), nullable=True),
        sa.PrimaryKeyConstraint('account_id'),
        sa.UniqueConstraint('account_name'),
        sa.UniqueConstraint('account_number')
    )

    op.create_table('auditlog',
        sa.Column('audit_log_event_id', mysql.INTEGER(unsigned=True), nullable=False, autoincrement=True),
        sa.Column('timestamp', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('actor', sa.String(length=100), nullable=False),
        sa.Column('event', sa.String(length=50), nullable=False),
        sa.Column('data', mysql.JSON(), nullable=False),
        sa.PrimaryKeyConstraint('audit_log_event_id')
    )
    op.create_index(op.f('ix_auditlog_event'), 'auditlog', ['event'], unique=False)

    op.create_table('config_namespaces',
        sa.Column('namespace_prefix', sa.String(length=100), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('sort_order', sa.SmallInteger(), server_default='2', nullable=False),
        sa.PrimaryKeyConstraint('namespace_prefix')
    )

    op.create_table('emails',
        sa.Column('email_id', mysql.INTEGER(), nullable=False, autoincrement=True),
        sa.Column('timestamp', mysql.DATETIME(), nullable=False),
        sa.Column('subsystem', sa.String(length=64), nullable=False),
        sa.Column('subject', sa.String(length=256), nullable=False),
        sa.Column('sender', sa.String(length=256), nullable=False),
        sa.Column('recipients', mysql.JSON(), nullable=False),
        sa.Column('uuid', sa.String(length=36), nullable=False),
        sa.Column('message_html', mysql.TEXT(), nullable=True),
        sa.Column('message_text', mysql.TEXT(), nullable=True),
        sa.PrimaryKeyConstraint('email_id')
    )

    # region Issues
    op.create_table('issue_properties',
        sa.Column('property_id', mysql.INTEGER(unsigned=True), nullable=False, autoincrement=True),
        sa.Column('issue_id', sa.String(length=256), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('value', mysql.JSON(), nullable=False),
        sa.PrimaryKeyConstraint('property_id', 'issue_id')
    )

    op.create_table('issue_types',
        sa.Column('issue_type_id', mysql.INTEGER(unsigned=True), nullable=False, autoincrement=True),
        sa.Column('issue_type', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('issue_type_id')
    )

    op.create_table('issues',
        sa.Column('issue_id', sa.String(length=256), nullable=False),
        sa.Column('issue_type_id', mysql.INTEGER(unsigned=True), nullable=True),
        sa.PrimaryKeyConstraint('issue_id')
    )
    op.create_index(op.f('ix_issues_issue_type_id'), 'issues', ['issue_type_id'], unique=False)
    # endregion

    op.create_table('logs',
        sa.Column('log_event_id', mysql.INTEGER(), nullable=False, autoincrement=True),
        sa.Column('level', sa.String(length=10), nullable=False),
        sa.Column('levelno', sa.SmallInteger(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('module', sa.String(length=255), nullable=False),
        sa.Column('filename', sa.String(length=255), nullable=False),
        sa.Column('lineno', mysql.INTEGER(), nullable=True),
        sa.Column('funcname', sa.String(length=255), nullable=False),
        sa.Column('pathname', sa.Text(), nullable=True),
        sa.Column('process_id', mysql.INTEGER(), nullable=True),
        sa.Column('stacktrace', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('log_event_id')
    )

    op.create_table('resource_properties',
        sa.Column('property_id', mysql.INTEGER(unsigned=True), nullable=False, autoincrement=True),
        sa.Column('resource_id', sa.String(length=256), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('value', mysql.JSON(), nullable=False),
        sa.PrimaryKeyConstraint('property_id', 'resource_id')
    )

    op.create_table('resource_types',
        sa.Column('resource_type_id', mysql.INTEGER(unsigned=True), nullable=False, autoincrement=True),
        sa.Column('resource_type', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('resource_type_id')
    )

    op.create_table('resources',
        sa.Column('resource_id', sa.String(length=256), nullable=False),
        sa.Column('account_id', mysql.INTEGER(), nullable=True),
        sa.Column('location', sa.String(length=50), nullable=True),
        sa.Column('resource_type_id', mysql.INTEGER(unsigned=True), nullable=True),
        sa.PrimaryKeyConstraint('resource_id')
    )
    op.create_index(op.f('ix_resources_account_id'), 'resources', ['account_id'], unique=False)
    op.create_index(op.f('ix_resources_location'), 'resources', ['location'], unique=False)
    op.create_index(op.f('ix_resources_resource_type_id'), 'resources', ['resource_type_id'], unique=False)

    op.create_table('roles',
        sa.Column('role_id', mysql.INTEGER(), nullable=False, autoincrement=True),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('color', sa.String(length=7), server_default='#9E9E9E', nullable=False),
        sa.PrimaryKeyConstraint('role_id'),
        sa.UniqueConstraint('name')
    )
    op.create_table('tags',
        sa.Column('tag_id', mysql.INTEGER(), nullable=False, autoincrement=True),
        sa.Column('resource_id', sa.String(length=256), nullable=False),
        sa.Column('key', sa.String(length=128), nullable=False),
        sa.Column('value', sa.String(length=256), nullable=False),
        sa.Column('created', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('tag_id'),
        sa.UniqueConstraint('tag_id', 'resource_id', 'key', name='uniq_tag_resource_id_key')
    )
    op.create_index(op.f('ix_tags_resource_id'), 'tags', ['resource_id'], unique=False)

    op.create_table('users',
        sa.Column('user_id', mysql.INTEGER(), nullable=False, autoincrement=True),
        sa.Column('username', sa.String(length=100), nullable=False),
        sa.Column('password', sa.String(length=73), nullable=True),
        sa.Column('auth_system', sa.String(length=50), server_default='builtin', nullable=False),
        sa.PrimaryKeyConstraint('user_id'),
        sa.UniqueConstraint('username', 'auth_system', name='uniq_username_authsys')
    )

    op.create_table('config_items',
        sa.Column('config_item_id', mysql.INTEGER(), nullable=False, autoincrement=True),
        sa.Column('key', sa.String(length=256), nullable=False),
        sa.Column('value', mysql.JSON(), nullable=False),
        sa.Column('type', sa.String(length=20), nullable=False),
        sa.Column('namespace_prefix', sa.String(length=100), server_default='default', nullable=False),
        sa.Column('description', sa.String(length=256), nullable=True),
        sa.ForeignKeyConstraint(['namespace_prefix'], ['config_namespaces.namespace_prefix'], name='fk_config_namespace_prefix', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('config_item_id'),
        sa.UniqueConstraint('key', 'namespace_prefix', name='uniq_key_namespace')
    )

    op.create_table('user_roles',
        sa.Column('user_role_id', mysql.INTEGER(), nullable=False, autoincrement=True),
        sa.Column('user_id', mysql.INTEGER(), nullable=True),
        sa.Column('role_id', mysql.INTEGER(), nullable=True),
        sa.ForeignKeyConstraint(['role_id'], ['roles.role_id'], name='fk_user_role_role', ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], name='fk_user_role_user', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('user_role_id')
    )

    if USE_PARTITIONING:
        for part in partitions:
            op.execute('ALTER TABLE {table} PARTITION BY KEY({key}) PARTITIONS {partitions}'.format(
                table=part.table,
                key=part.key,
                partitions=part.partitions
            ))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_roles')
    op.drop_table('config_items')
    op.drop_table('users')
    op.drop_index(op.f('ix_tags_resource_id'), table_name='tags')
    op.drop_table('tags')
    op.drop_table('roles')
    op.drop_index(op.f('ix_resources_resource_type_id'), table_name='resources')
    op.drop_index(op.f('ix_resources_location'), table_name='resources')
    op.drop_index(op.f('ix_resources_account_id'), table_name='resources')
    op.drop_table('resources')
    op.drop_table('resource_types')
    op.drop_table('resource_properties')
    op.drop_table('logs')
    op.drop_index(op.f('ix_issues_issue_type_id'), table_name='issues')
    op.drop_table('issues')
    op.drop_table('issue_types')
    op.drop_table('issue_properties')
    op.drop_table('emails')
    op.drop_table('config_namespaces')
    op.drop_index(op.f('ix_auditlog_event'), table_name='auditlog')
    op.drop_table('auditlog')
    op.drop_table('accounts')
    # ### end Alembic commands ###

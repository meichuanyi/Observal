"""Add registered_agents_only column to organizations.

When enabled, only registered (active) agents are traced.
Unregistered agent telemetry is stored as metadata-only (no content).

Revision ID: 0019
Revises: 0018
Create Date: 2026-05-01
"""

from alembic import op

revision = "0019"
down_revision = "0018"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns
                WHERE table_name = 'organizations' AND column_name = 'registered_agents_only'
            ) THEN
                ALTER TABLE organizations ADD COLUMN registered_agents_only BOOLEAN NOT NULL DEFAULT FALSE;
            END IF;
        END
        $$;
    """)


def downgrade() -> None:
    op.execute("""
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1 FROM information_schema.columns
                WHERE table_name = 'organizations' AND column_name = 'registered_agents_only'
            ) THEN
                ALTER TABLE organizations DROP COLUMN registered_agents_only;
            END IF;
        END
        $$;
    """)

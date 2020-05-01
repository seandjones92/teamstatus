#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE TABLE users(
        ID SERIAL PRIMARY KEY   NOT NULL,
        SLACKID         TEXT    NOT NULL,
        NAME            TEXT    NOT NULL,
        LASTUPDATED     DATE    NOT NULL,
        STATUS          INTEGER NOT NULL
    );
    CREATE TABLE status(
        ID SERIAL PRIMARY KEY   NOT NULL,
        LONGSTAT        TEXT    NOT NULL,
        SHORTSTAT       TEXT    NOT NULL,
        EMOJI           TEXT    NOT NULL
    )
EOSQL

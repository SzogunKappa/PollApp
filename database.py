from typing import Tuple, List
Poll = Tuple[int, str, str]
Vote = Tuple[str, int]
Option = Tuple[int, str, int]

CREATE_POLLS = """CREATE TABLE IF NOT EXISTS polls
(id SERIAL PRIMARY KEY, title TEXT, owner_username TEXT);"""
CREATE_OPTIONS = """CREATE TABLE IF NOT EXISTS options
(id SERIAL PRIMARY KEY, option_text TEXT, poll_id INTEGER, FOREIGN KEY(poll_id) REFERENCES polls (id));"""
CREATE_VOTES = """CREATE TABLE IF NOT EXISTS votes
(username TEXT, option_id INTEGER, vote_timestamp INTEGER, FOREIGN KEY(option_id) REFERENCES options (id));"""

SELECT_POLL ="SELECT * FROM polls WHERE id = %s;"
SELECT_ALL_POLLS = "SELECT * FROM polls;"
SELECT_POLL_OPTIONS = """SELECT * FROM options WHERE poll_id = %s;"""
SELECT_NEWEST_POLL = """SELECT * FROM polls
WHERE polls.id = (
    SELECT id FROM polls ORDER BY id DESC LIMIT 1
);"""

SELECT_OPTION = "SELECT * FROM options WHERE id = %s;"
SELECT_VOTES_FOR_OPTION = "SELECT * FROM votes WHERE option_id = %s"

INSERT_OPTION_RETURNING_ID = "INSERT INTO options (option_text, poll_id) VALUES (%s, %s) RETURNING id;"
INSERT_VOTE = "INSERT INTO votes (username, option_id, vote_timestamp) VALUES (%s, %s, %s);"

INSERT_POLL_RETURN_ID = """INSERT INTO polls (title, owner_username) VALUES (%s, %s) RETURNING id;"""

COUNT_VOTES_BY_POLL_ID = "SELECT COUNT(*) " \
                         "FROM votes LEFT JOIN options ON votes.option_id = options.id " \
                         "WHERE poll_id = %s GROUP BY poll_id  "

def get_poll_votes_count(connection, poll_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(COUNT_VOTES_BY_POLL_ID, (poll_id,))
            vote_count = cursor.fetchone()[0]
            return vote_count

def create_tables(connection):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_POLLS)
            cursor.execute(CREATE_OPTIONS)
            cursor.execute(CREATE_VOTES)

#       --polls--
def create_poll(connection, title, owner):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_POLL_RETURN_ID,(title, owner))
            poll_id = cursor.fetchone()[0]
            return poll_id

def get_poll(connection, poll_id: int) -> Poll:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_POLL, (poll_id,))
            return cursor.fetchone()

def get_polls(connection):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_POLLS)
            return cursor.fetchall()


def get_latest_poll(connection):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_NEWEST_POLL)
            return cursor.fetchone()

def get_poll_options(connection, poll_id) -> List[Option]:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_POLL_OPTIONS, (poll_id,))
            return cursor.fetchall()
# -- options --
def get_option(connection, option_id: int) -> Option:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_OPTION, (option_id,))
            return cursor.fetchone()

def add_option(connection, option_text, poll_id: int):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_OPTION_RETURNING_ID, (option_text, poll_id))
            option_id = cursor.fetchone
            return option_id

# -- votes --
def get_votes_for_option(connection, option_id: int) -> List[Vote]:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_VOTES_FOR_OPTION,(option_id,))
            return cursor.fetchall()


def add_poll_vote(connection, username, vote_timestamp: float, option_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_VOTE, (username, option_id, vote_timestamp))
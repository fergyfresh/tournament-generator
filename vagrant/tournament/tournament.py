#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

DBNAME = 'tournament'

def connect(dbname=DBNAME):
    #Connect to the db and return the connection
    return psycopg2.connect('dbname=' + dbname)

def commitQuery(query, dbname=DBNAME):
    """Connects, sends query, executes, commits, and closes.
    Returns the databse object."""
    db = connect(dbname)
    c = db.cursor()
    c.execute(query)
    db.commit()
    db.close()
    return db

def deleteMatches():
    # Removes all match records from the db.
    commitQuery("""
    DELETE FROM matches;
    """)

def deletePlayers():
    # Removes all player records from the db.
    commitQuery("""
    DELETE FROM players;
    """)

def countPlayers():
    # Returns the number of registered players.
    query = """
    SELECT COUNT(id) from players;
    """
    db = connect()
    c = db.cursor()
    c.execute(query)
    result = c.fetchall()
    db.close()
    assert len(result) == 1
    return int(result[0][0])

def registerPlayer(name):
    """
    Adds a player record to the database.

    @type  name: string
    @param name: player's full name
    """
    add_query = """
    INSERT INTO players (name) VALUES (%s)
    """
    db = connect()
    c = db.cursor()
    c.execute(add_query, (name,))
    db.commit()
    db.close()

def playerStandings():
    """Descending list of player win/loss stats.

    Returns a list of the players and their win records, sorted descendingly
    by wins. There is no distinction between ties.

    @rtype:  list(int, string, int, int)
    @return: list(id, name, wins, matches)

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()
    c.execute("""
    select winners.id, winners.name, wins, wins+losses as matches
    from (
    select players.id, name, count(matches.id) as wins
        from players left join matches
            on players.id = winner_id
        group by players.id
        order by wins desc
    ) as winners left join (
    select players.id, name, count(matches.id) as losses
        from players left join matches
            on players.id = loser_id
        group by players.id
        order by losses desc
    ) as losers
            on winners.id = losers.id;
    """)
    results = c.fetchall()
    db.close()
    return results

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    @type  winner: int
    @param winner: match winner's player id
    @type  loser: int
    @param loser: match winner's player id

    """
    db = connect()
    c = db.cursor()

    query = """
    SELECT COUNT(id) from players;
    """
    c.execute("""
    INSERT INTO matches (winner_id, loser_id)
    VALUES (%s, %s)""", (winner, loser))
    db.commit()
    db.close()

def swissPairings():
    """Returns a list of player pairings for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    @rtype:  list(int, string, int, string)
    @return: list(id1, name1, id2, name2)

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = [(record[0], record[1]) for record in playerStandings()]
    if len(standings) < 2:
        raise KeyError("Not enough players.")
    left = standings[0::2]
    right = standings[1::2]
    pairings = zip(left, right)

    # flatten the pairings and convert back to a tuple
    results = [tuple(list(sum(pairing, ()))) for pairing in pairings]

    return results

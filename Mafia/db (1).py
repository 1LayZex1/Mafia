import sqlite3
from random import shuffle

def insert_player(player_id, username):
    con = sqlite3.connect('db.db')
    cur = con.cursor()
    sql = f"INSERT INTO players (player_id, username) VALUES ('{player_id}', '{username}')"
    cur.execute(sql)
    con.commit()
    con.close()


def players_amount():
    con = sqlite3.connect('db.db')
    cur = con.cursor()
    sql = f"SELECT * FROM players"
    cur.execute(sql)
    res = cur.fetchall()
    con.close()
    return len(res)

def get_mafia_usernames():
    con = sqlite3.connect('db.db')
    cur = con.cursor()
    sql = f"SELECT username FROM PLAYERS where role = 'mafia'"
    cur.execute(sql)
    data = cur.fetchall()
    names = ''
    for row in data:
        name = row[0]
        names += name + '\n'
    con.close()
    return names


def get_players_roles():
    con = sqlite3.connect('db.db')
    cur = con.cursor()
    sql = f"SELECT player_id, role FROM PLAYERS"
    cur.execute(sql)
    data = cur.fetchall()
    con.close()
    return data




def get_all_alive():
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    sql = f"SELECT username FROM players WHERE dead = 0"
    cur.execute(sql)
    res = cur.fetchall()
    data = [row[0] for row in data]
    con.close()
    return data


def set_roles():
    game_roles = ['citizen'] * players
    mafias = int(players * 0.3)
    for i in range(mafias):
        game_roles[i] = 'mafia'
    random.shuffle(game_roles)
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    sql = f"SELECT player_id FROM PLAYERS"
    player_ids_rows = cur.fetchall()
    for role, row in zip(game_roles, player_ids_rows):
        sql = f"UPDATE players SET role = '{role}' WHERE player_id = '{row[0]}'"
        cur.execute(sql)
    con.commit()
    con.close()


def vote(type, username, player_id):
    # type = 'mafia_vote, citizen_vote'
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    cur.execute(
        f"SELECT username FROM players WHERE player_id = '{player_id}' and dead = 0 and voted = 0")
    can_vote = cur.fetchone()
    if can_vote:
        cur.execute(
            f"UPDATE players SET {type} + 1 WHERE username = '{username}'")
        cur.execute(
            f"UPDATE players SET voted = 1 WHERE player_id = '{player_id}'")
        con.commit()
        con.close()
        return True
    con.close()
    return False


def mafia_kill():
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    #Choose who has the largest number of votes from mafias
    sql = f"SELECT MAX(mafia_vote) FROM players"
    max_votes = cur.fetchone()[0]
    #Choose number of mafias, whose != dead
    cur.execute(
        f"SELECT COUNT(*) FROM players WHERE dead = 0 and role = 'mafia'")
    mafia_alive = cur.fetchone()[0]
    username_killed = 'никого'
    #Max amount of votes must be equal with number of mafias
    if max_votes == mafia_alive:
        #Get username who has the largest votes
        cur.execute(
            f"SELECT username FROM players WHERE mafia_vote = '{max_votes}'")
        username_killed = cur.fetchone()[0]
        #Update Bd, show his death
        cur.execute(
            f"UPDATE players SET dead = 1 WHERE username = '{username_killed}'")
        con.commit()
    con.close()
    return username_killed


def citizen_kill():
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    #Choose the largest number citizen_vote
    sql = f"SELECT MAX(citizen_vote) FROM players"
    max_votes = cur.fetchone()[0]
    #Choose amount alive citizens
    cur.execute(
        f"SELECT COUNT(*) FROM players WHERE citizen_vote = '{max_votes}'")
    max_votes_count = cur.fetchone()[0]
    username_killed = 'Никого'
    #Check person with max votes
    if max_votes_count == 0:
        cur.execute(
            f"SELECT username FROM players WHERE citizen_vote = '{max_votes}'")
        username_killed = cur.fetchone()[0]
        cur.execute(
            f"UPDATE players SET dead = 1 WHERE username = '{username_killed}'")     
        con.commit()
    con.close()
    return username_killed


def check_winner():
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM players WHERE role = 'mafia' and dead = 0")
    mafia_alive = cur.fetchone()[0]
    cur.execute(
        "SELECT COUNT(*) FROM plauers WHERE role != 'mafia' and dead = 0")
    citizen_alive = cur.fetchone()[0]
    if mafia_alive >= citizen_alive:
        return 'Мафия'
    if mafia_alive == 0:
        return 'Горожане'


#Random role
lst = [1, 2, 3, 4, 5, 6]
shuffle(lst)
print(lst)
  
for role, player_id in zip(game_roles, player_ids):
    sql = f"UPDATE players SET role = '{role}' WHERE player_id = {player_id}"
    cur.execute(sql)
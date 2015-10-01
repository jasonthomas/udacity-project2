from tournament import *  # noqa

numplays = 0
totalplays = 8


# simulate win
def win():
    import random
    winner = random.choice([0, 2])
    if winner == 2:
        loser = 0
    else:
        loser = 2

    return winner, loser


# simulate play
def play():
    swiss = swissPairings()

    for i in swiss:
        print i
        winner, loser = win()
        reportMatch(i[winner], i[loser])

    print playerStandings()

deletePlayers()

player = [
    "Jason",
    "Bincy",
    "Benita",
    "Daniel",
    "Connie",
    "Dennis",
    "Emily",
    "Thomas",
    "Sosamma",
    "Benjamin",
    "Susan",
    "Sam",
    "William",
    "Anthony",
    "Alex",
    "Sasha",
]

for user in player:
    registerPlayer(user)


while numplays < totalplays:
    play()
    numplays += 1

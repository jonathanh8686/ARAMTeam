#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cassiopeia as cass
import random
import arrow
from cassiopeia.core import Summoner, MatchHistory, Match
from cassiopeia import Queue, Patch, Match, Season
from cassiopeia.data import Role, Lane, Division, Tier
import json
import matplotlib.pyplot as plt

conf = json.loads(open("config.json", "r").read())

cass.set_riot_api_key(conf["API_KEY"])
cass.set_default_region("NA")


users = ["Catalysis"]
seenUsers = set()


while(len(users) != 0):

    cuser = users[0]
    seenUsers.add(users[0])

    users.pop(0)
    matches = cass.MatchHistory(summoner=Summoner(name=cuser, region="NA"), queues=["ARAM"])
    print(len(matches))

    fullgames = json.loads(open("matches.dat", "r").read())
    seen = set()
    for g in fullgames:
        seen.add(g["id"])

    print("Already found " + str(len(fullgames)) + " matches...")

    for match in matches[5:]:
        try:
            if(match.id in seen):
                continue
            seen.add(match.id)

            gameObject = {
                "id": match.id,
                "blueteam": [x.champion.id for x in match.blue_team.participants],
                "redteam": [x.champion.id for x in match.red_team.participants],
                "result": int(match.blue_team.win)
            }

            for p in match.blue_team.participants:
                if(p.summoner.name in seenUsers):
                    continue
                seenUsers.add(p.summoner.name)
                users.append(p.summoner.name)

            for p in match.red_team.participants:
                if(p.summoner.name in seenUsers):
                    continue
                seenUsers.add(p.summoner.name)
                users.append(p.summoner.name)

            fullgames.append(gameObject)
            print(gameObject, end="\n\n")
        except KeyboardInterrupt:
            raise
        except:
            continue

    print("Updated to " + str(len(fullgames)) + " matches!")

    open("matches.dat", "w").write(json.dumps(fullgames))



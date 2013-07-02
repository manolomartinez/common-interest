import commoninterest as ci
import json
import os
import pickle
import time

def findgames(dimension): # The way I use this function is as follows: 
    # I uncomment lines 27-64, and comment lines 14-23. Run the function and
    # kill it with ^C. This creates the pickled files. Then I comment and
    # uncomment again until it is as shown here. This way I can halt the
    # calculation whenever I want (with ^C). This creates pickled files which
    # are read whenever I resume.
    with open("pickledsender", "rb") as psender:
        gamessender = pickle.load(psender)
    with open("pickledreceiver", "rb") as preceiver:
        gamesreceiver = pickle.load(preceiver)
    with open("pickledpairsender", "rb") as psender:
        pairsender = pickle.load(psender)
    with open("pickledpairreceiver", "rb") as preceiver:
        pairreceiver = pickle.load(preceiver)
    with open("pickledpossiblepairs", "rb") as pp:
        possible_pairs = pickle.load(pp)
    try:
        possible_cstars = []
        
        #possible_pairs = []
        #pairsender = []
        #pairreceiver = []
        #gamessender = {}
        #gamesreceiver = {}
        timestr = time.strftime("%d%b%H-%M")
        #for pair in pairsender:
            #gamessender[str(pair)] = []
            #gamesreceiver[str(pair)] = []
        #game = ci.Game(ci.payoffs(dimension))
        #gamepairsender = [game.cistar, game.starsender]
        #gamepairreceiver = [game.cistar, game.starreceiver]
        #if gamepairsender not in possible_pairs or gamepairreceiver not in possible_pairs:
            #equilibria = game.just_equilibria()
            #if gamepairsender not in possible_pairs:
                #ppold = possible_pairs
                #possible_pairs.append(gamepairsender)
                #pairsender.append(gamepairsender)
                #pairreceiver.append(gamepairsender)
                #gamessender[str(gamepairsender)] = []
                #gamesreceiver[str(gamepairsender)] = []
                #gameentry = {}
                #gameentry[str(game.payoffs)] = equilibria
                #gamessender[str(gamepairsender)].append(gameentry)
                #print("sender", gamepairsender,
                      #len(gamessender[str(gamepairsender)]))
            #if gamepairreceiver not in ppold:
                #if gamepairreceiver not in possible_pairs:
                    #possible_pairs.append(gamepairreceiver)
                #pairreceiver.append(gamepairreceiver)
                #pairsender.append(gamepairreceiver)
                #gamesreceiver[str(gamepairreceiver)] = []
                #gamessender[str(gamepairreceiver)] = []
                #gameentry = {}
                #gameentry[str(game.payoffs)] = equilibria
                #gamesreceiver[str(gamepairreceiver)].append(gameentry)
                #print("receiver", gamepairreceiver,
                      #len(gamesreceiver[str(gamepairreceiver)]))

        while pairsender != [] or pairreceiver != []:
            game = ci.Game(ci.payoffs(dimension))
            gamepairsender = [game.cistar, game.starsender]
            gamepairreceiver = [game.cistar, game.starreceiver]
            if gamepairsender not in possible_pairs or gamepairreceiver not in possible_pairs or gamepairsender in pairsender or gamepairreceiver in pairreceiver:
                equilibria = game.just_equilibria()
                if gamepairsender not in possible_pairs:
                    possible_pairs.append(gamepairsender)
                    pairsender.append(gamepairsender)
                    pairreceiver.append(gamepairsender)
                    gamessender[str(gamepairsender)] = []
                    gamesreceiver[str(gamepairsender)] = []
                if gamepairreceiver not in possible_pairs:
                    possible_pairs.append(gamepairreceiver)
                    pairsender.append(gamepairreceiver)
                    gamessender[str(gamepairreceiver)] = []
                    pairreceiver.append(gamepairreceiver)
                    gamesreceiver[str(gamepairreceiver)] = []
                for pair in pairsender:
                    if gamepairsender == pair:
                        gameentry = {}
                        gameentry[str(game.payoffs)] = equilibria
                        gamessender[str(pair)].append(gameentry)
                        print("sender", pair, len(gamessender[str(pair)]))
                        if len(gamessender[str(pair)]) > 1499:
                            pairsender.remove(pair)
                            print("sender", pair, "done.")
                            filename = ''.join(["sender", str(pair), timestr])
                            with open(filename, 'w') as senderpair:
                                json.dump(gamessender[str(pair)], senderpair)
                for pair in pairreceiver:
                    if gamepairreceiver == pair:
                        gameentry = {}
                        gameentry[str(game.payoffs)] = equilibria
                        gamesreceiver[str(pair)].append(gameentry)
                        print("receiver", pair, len(gamesreceiver[str(pair)]))
                        if len(gamesreceiver[str(pair)]) > 1499:
                            pairreceiver.remove(pair)
                            print("receiver", pair, "done.")
                            filename = ''.join(["receiver", str(pair), timestr])
                            with open(filename, 'w') as receiverpair:
                                json.dump(gamesreceiver[str(pair)], receiverpair)
        with open("gamessender", "w") as senderfile:
            json.dump(gamessender, senderfile)
        with open("gamesreceiver", "w") as receiverfile:
            json.dump(gamesreceiver, receiverfile)
        with open("pickledsender", "wb") as psender:
            pickle.dump(gamessender, psender)
        with open("pickledreceiver", "wb") as preceiver:
            pickle.dump(gamesreceiver, preceiver)
        with open("pickledpairsender", "wb") as psender:
            pickle.dump(pairsender, psender)
        with open("pickledpairreceiver", "wb") as preceiver:
            pickle.dump(pairreceiver, preceiver)
        with open("pickledpossiblepairs", "wb") as pp:
            pickle.dump(possible_pairs, pp)

    except KeyboardInterrupt:
        with open("pickledsender", "wb") as psender:
            pickle.dump(gamessender, psender)
        with open("pickledreceiver", "wb") as preceiver:
            pickle.dump(gamesreceiver, preceiver)
        with open("pickledpairsender", "wb") as psender:
            pickle.dump(pairsender, psender)
        with open("pickledpairreceiver", "wb") as preceiver:
            pickle.dump(pairreceiver, preceiver)
        with open("pickledpossiblepairs", "wb") as pp:
            pickle.dump(possible_pairs, pp)


def findgames_CKnostar(dimension):
    with open("pickledsender", "rb") as psender:
        gamessender = pickle.load(psender)
    with open("pickledreceiver", "rb") as preceiver:
        gamesreceiver = pickle.load(preceiver)
    with open("pickledpairsender", "rb") as psender:
        pairsender = pickle.load(psender)
    with open("pickledpairreceiver", "rb") as preceiver:
        pairreceiver = pickle.load(preceiver)
    with open("pickledpossiblepairs", "rb") as pp:
        possible_pairs = pickle.load(pp)
    with open("pickledcs", "rb") as pp:
        possible_cs = pickle.load(pp)
    with open("pickledgames", "rb") as pp:
        games = pickle.load(pp)
    try:
        #possible_cs = []
        #possible_pairs = []
        #pairsender = []
        #pairreceiver = []
        #games = {}
        #gamessender = {}
        #gamesreceiver = {}
        timestr = time.strftime("%d%b%H-%M")
        #for pair in pairsender:
            #gamessender[str(pair)] = []
            #gamesreceiver[str(pair)] = []
        #game = ci.Game(ci.payoffs(dimension))
        #gamec = game.kendalldistance
        #gamepairsender = [game.kendalldistance, game.kendallsender]
        #gamepairreceiver = [game.kendalldistance, game.kendallreceiver]
        #if gamepairsender not in possible_pairs or gamepairreceiver not in possible_pairs:
            #equilibria = game.just_equilibria()
            #if gamepairsender not in possible_pairs:
                #ppold = possible_pairs
                #possible_cs.append(gamec)
                #possible_pairs.append(gamepairsender)
                #pairsender.append(gamepairsender)
                #pairreceiver.append(gamepairsender)
                #gamessender[str(gamepairsender)] = []
                #gamesreceiver[str(gamepairsender)] = []
                #games[str(gamec)] = []
                #gameentry = {}
                #gameentry[str(game.payoffs)] = equilibria
                #gamessender[str(gamepairsender)].append(gameentry)
                #games[str(gamec)].append(gameentry)
                #print("sender", gamepairsender,
                      #len(gamessender[str(gamepairsender)]))
            #if gamepairreceiver not in ppold:
                #if gamepairreceiver not in possible_pairs:
                    #possible_pairs.append(gamepairreceiver)
                #pairreceiver.append(gamepairreceiver)
                #pairsender.append(gamepairreceiver)
                #gamesreceiver[str(gamepairreceiver)] = []
                #gamessender[str(gamepairreceiver)] = []
                #gameentry = {}
                #gameentry[str(game.payoffs)] = equilibria
                #gamesreceiver[str(gamepairreceiver)].append(gameentry)
                #print("receiver", gamepairreceiver,
                      #len(gamesreceiver[str(gamepairreceiver)]))

        while pairsender != [] or pairreceiver != []:
            game = ci.Game(ci.payoffs(dimension))
            gamec = game.kendalldistance
            gamepairsender = [game.kendalldistance, game.kendallsender]
            gamepairreceiver = [game.kendalldistance, game.kendallreceiver]
            if gamepairsender not in possible_pairs or gamepairreceiver not in possible_pairs or gamepairsender in pairsender or gamepairreceiver in pairreceiver:
                equilibria = game.just_equilibria()
                #if gamec not in possible_cs:
                    #possible_cs.append(gamec)
                    #games[str(gamec)] = []
                if gamepairsender not in possible_pairs:
                    possible_pairs.append(gamepairsender)
                    pairsender.append(gamepairsender)
                    pairreceiver.append(gamepairsender)
                    gamessender[str(gamepairsender)] = []
                    gamesreceiver[str(gamepairsender)] = []
                if gamepairreceiver not in possible_pairs:
                    possible_pairs.append(gamepairreceiver)
                    pairsender.append(gamepairreceiver)
                    gamessender[str(gamepairreceiver)] = []
                    pairreceiver.append(gamepairreceiver)
                    gamesreceiver[str(gamepairreceiver)] = []
                for pair in pairsender:
                    if gamepairsender == pair:
                        gameentry = {}
                        gameentry[str(game.payoffs)] = equilibria
                        gamessender[str(pair)].append(gameentry)
                        print("sender", pair, len(gamessender[str(pair)]))
                        if len(gamessender[str(pair)]) > 1499:
                            pairsender.remove(pair)
                            print("sender", pair, "done.")
                            filename = ''.join(["sender", str(pair), timestr])
                            with open(filename, 'w') as senderpair:
                                json.dump(gamessender[str(pair)], senderpair)
                for pair in pairreceiver:
                    if gamepairreceiver == pair:
                        gameentry = {}
                        gameentry[str(game.payoffs)] = equilibria
                        gamesreceiver[str(pair)].append(gameentry)
                        print("receiver", pair, len(gamesreceiver[str(pair)]))
                        if len(gamesreceiver[str(pair)]) > 1499:
                            pairreceiver.remove(pair)
                            print("receiver", pair, "done.")
                            filename = ''.join(["receiver", str(pair), timestr])
                            with open(filename, 'w') as receiverpair:
                                json.dump(gamesreceiver[str(pair)], receiverpair)
                #for c in possible_cs:
                    #if gamec == c:
                        #gameentry = {}
                        #gameentry[str(game.payoffs)] = equilibria
                        #games[str(c)].append(gameentry)
                        #print("c", c, len(games[str(c)]))
                        #if len(games[str(c)]) > 1499:
                            #possible_cs.remove(c)
                            #print("c", c, "done.")
                            #filename = ''.join(["c", str(c), timestr])
                            #with open(filename, 'w') as cs:
                                #json.dump(games[str(c)], cs)


        with open("gamessender", "w") as senderfile:
            json.dump(gamessender, senderfile)
        with open("gamesreceiver", "w") as receiverfile:
            json.dump(gamesreceiver, receiverfile)
        with open("pickledsender", "wb") as psender:
            pickle.dump(gamessender, psender)
        with open("pickledreceiver", "wb") as preceiver:
            pickle.dump(gamesreceiver, preceiver)
        with open("pickledpairsender", "wb") as psender:
            pickle.dump(pairsender, psender)
        with open("pickledpairreceiver", "wb") as preceiver:
            pickle.dump(pairreceiver, preceiver)
        with open("pickledpossiblepairs", "wb") as pp:
            pickle.dump(possible_pairs, pp)
        with open("pickledcs", "wb") as pp:
            pickle.dump(possible_cs, pp)
        with open("pickledgames", "wb") as pp:
            pickle.dump(games, pp)

    except KeyboardInterrupt:
        with open("pickledsender", "wb") as psender:
            pickle.dump(gamessender, psender)
        with open("pickledreceiver", "wb") as preceiver:
            pickle.dump(gamesreceiver, preceiver)
        with open("pickledpairsender", "wb") as psender:
            pickle.dump(pairsender, psender)
        with open("pickledpairreceiver", "wb") as preceiver:
            pickle.dump(pairreceiver, preceiver)
        with open("pickledpossiblepairs", "wb") as pp:
            pickle.dump(possible_pairs, pp)
        with open("pickledcs", "wb") as pp:
            pickle.dump(possible_cs, pp)
        with open("pickledgames", "wb") as pp:
            pickle.dump(games, pp)

def findgames_Cnostar(dimension):
    with open("pickledoutcs", "rb") as pp:
        outstanding_cs = pickle.load(pp)
    with open("pickledcs", "rb") as pp:
        possible_cs = pickle.load(pp)
    with open("pickledgames", "rb") as pp:
        games = pickle.load(pp)

    try:
        #possible_cs = []
        #outstanding_cs = []
        #games = {}
        timestr = time.strftime("%d%b%H-%M")
        #game = ci.Game(ci.payoffs(dimension))
        #gamec = game.cistar
        #if gamec not in possible_cs:
            #equilibria = game.just_equilibria()
            #possible_cs.append(gamec)
            #outstanding_cs.append(gamec)
            #games[str(gamec)] = []
            #gameentry = {}
            #gameentry[str(game.payoffs)] = equilibria
            #games[str(gamec)].append(gameentry)
        while outstanding_cs != []:
            game = ci.Game(ci.payoffs(dimension))
            gamec = game.cistar
            if gamec not in possible_cs or gamec in outstanding_cs:
                equilibria = game.just_equilibria()
                if gamec not in possible_cs:
                    possible_cs.append(gamec)
                    outstanding_cs.append(gamec)
                    games[str(gamec)] = []
                for c in possible_cs:
                    if gamec == c:
                        gameentry = {}
                        gameentry[str(game.payoffs)] = equilibria
                        games[str(c)].append(gameentry)
                        print("c", c, len(games[str(c)]))
                        if len(games[str(c)]) > 1499:
                            outstanding_cs.remove(c)
                            print("c", c, "done.")
                            filename = ''.join(["c", str(c), timestr])
                            with open(filename, 'w') as cs:
                                json.dump(games[str(c)], cs)
        with open("pickledoutcs", "wb") as pp:
            pickle.dump(outstanding_cs, pp)
        with open("pickledcs", "wb") as pp:
            pickle.dump(possible_cs, pp)
        with open("pickledgames", "wb") as pp:
            pickle.dump(games, pp)

    except KeyboardInterrupt:
        with open("pickledoutcs", "wb") as pp:
            pickle.dump(outstanding_cs, pp)
        with open("pickledcs", "wb") as pp:
            pickle.dump(possible_cs, pp)
        with open("pickledgames", "wb") as pp:
            pickle.dump(games, pp)



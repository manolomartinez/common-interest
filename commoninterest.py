# Copyright (C) 2013  Manolo Martínez <manolomartinez@ub.edu>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#!/usr/bin/python3

import itertools
import json
import math
import pdb
import random
import subprocess


class Game:
    def __init__(self, payoffs): # Depending on what you are calculating,
        #comment or uncomment stuff here.
        self.dimension = int(math.sqrt(len(payoffs)/2))
        # The dimension of the (square) game
        self.chances = [1/self.dimension for i in range(self.dimension)]
        # Equiprobable states
        self.payoffs = payoffs
        self.sender, self.receiver = fromlisttomatrix(
            self.payoffs, self.dimension)
        #self.cstar = round(self.aggregate_ci_star(0), 2)
        self.c = round(self. aggregate_kendall_distance(0), 2)
        self.ks, self.kr = self.intrakendall(0)
        #self.ksstar, self.krstar = self.intrakendallstar()

    def intrakendallstar(self, tievalue): # This function calculates Kr* and
        # Ks*. Tievalue is the value we wish to give to the comparison between
        # a tie in one player and a strict preference in the other; 0
        # (equivalent to total agreement), 1 (eq. to total disagreement) and
        # 0.5 (something in between) are typical values.
        def kendall(state1, state2):
            state1plusmean = state1 + [sum(state1)/len(state1)]
            state2plusmean = state2 + [sum(state2)/len(state2)]
            return sum(
                [points(
                    state1plusmean, state2plusmean, pair[0], pair[1], tievalue)
                    for pair in itertools.combinations(
                        range(self.dimension + 1), 2)])
        skendalls = [kendall(
            self.sender[pair[0]], self.sender[pair[1]]) for
            pair in itertools.combinations(range(self.dimension), 2)]
        rkendalls = [kendall(self.receiver[pair[0]], self.receiver[pair[1]])
                     for pair in itertools.combinations(
                         range(self.dimension), 2)]
        return round(sum(
            skendalls)/len(skendalls), 2), round(
                sum(rkendalls)/len(rkendalls), 2)

    def intrakendall(self, tievalue): # Calculates Kr and Ks
        def kendall(state1, state2):
            return sum([points(state1, state2, pair[0], pair[1], tievalue) for pair in
                        itertools.combinations(range(self.dimension), 2)])
        skendalls = [kendall(self.sender[pair[0]], self.sender[pair[1]]) for
            pair in itertools.combinations(range(self.dimension), 2)]
        rkendalls = [kendall(self.receiver[pair[0]], self.receiver[pair[1]]) for
            pair in itertools.combinations(range(self.dimension), 2)]
        return round(sum(skendalls)/len(skendalls),2), round(sum(rkendalls)/len(rkendalls), 2)

    def aggregate_kendall_distance(self, tievalue): # Calculates C
        return sum(
            [self.chances[state] * self.kendall_tau_distance(state, tievalue) for state in range(self.dimension)])

    def kendall_tau_distance(self, state, tievalue):
        kendall =  sum([points(self.sender[state], self.receiver[state],
            pair[0], pair[1], tievalue) for pair in
            itertools.combinations(range(self.dimension), 2)])
        return kendall

    def aggregate_ci_star(self, tievalue): # Calculates C*
        return sum([self.chances[state] * self.common_interest_star(state,
                                                                    tievalue) for
            state in range(self.dimension)])
        #return [self.common_interest_star(state) for state in
                #range(self.dimension)]

    def common_interest_star(self, state, tievalue):
        senderplusmean = self.sender[state] + [sum(self.sender[state])/len(self.sender[state])]
        receiverplusmean = self.receiver[state] + [sum(self.receiver[state])/len(self.receiver[state])]
        #print(senderplusmean, receiverplusmean)
        kendall =  sum([points(senderplusmean, receiverplusmean,
            pair[0], pair[1], tievalue) for pair in
            itertools.combinations(range(self.dimension + 1), 2)])
        return kendall

    def just_equilibria(self): # Calls gambit and outputs the equilibria of the
        # game
        gambitgame = bytes(self.write_efg(), "utf-8")
        calc_eqs = subprocess.Popen(['gambit-lcp', '-d', '3', '-q'], stdin = subprocess.PIPE,
        #calc_eqs = subprocess.Popen(['gambit-lcp'], stdin = subprocess.PIPE,
                stdout = subprocess.PIPE)
        result = calc_eqs.communicate(input = gambitgame)[0]
        equilibria = str(result, "utf-8").split("\n")[:-1]
        return equilibria

    def info_in_equilibria(self): # Also returns the max mutual info between
        #states and messages; messages and acts; and states and acts.
        gambitgame = bytes(self.write_efg(), "utf-8")
        calc_eqs = subprocess.Popen(['gambit-lcp', '-d', '3', '-q'], stdin = subprocess.PIPE,
        #calc_eqs = subprocess.Popen(['gambit-lcp'], stdin = subprocess.PIPE,
                stdout = subprocess.PIPE)
        result = calc_eqs.communicate(input = gambitgame)[0]
        equilibria = str(result, "utf-8").split("\n")[:-1]
        sinfos, rinfos, jinfos = self.calculate_info_content(equilibria)
        return equilibria, max(sinfos), max(rinfos), max(jinfos)

    def payoffs_for_efg(self):
        payoffs = [[','.join([str(sact), str(ract)]) for sact, ract in
            zip(sstate, rstate)] for sstate, rstate in zip(self.sender,
                self.receiver)]
        return payoffs

    def actually_write_efg(self, filename): # Normally we do not really write
        #gambit .efg files. This is here in case we need to do it.
        with open(filename, 'w') as output:
            output.write(self.write_efg())
        
    def write_efg(self): # An artisanal API. Takes payoffs and outputs a file
        # gambit can understand
        dimension = self.dimension
        chance = [str(i) for i in self.chances]
        players = self.payoffs_for_efg()
        filelist = []
        filelist.append(r'EFG 2 R "Untitled Extensive Game" { "Player 1" "Player 2" }')
        filelist.append("\n")
        filelist.append(r'""')
        filelist.append("\n")
        filelist.append('')
        filelist.append("\n")

        # The Chance Player line
        line = "c \"\" 1 \"\" {"
        for element in range(len(chance)):
            line = line + " \"" + str(element + 1) + "\" " + str(chance[element])
        line = line + " } 0\n"
        filelist.append(line)

        # A Couple of Useful Strings
        statesstr = "{ "
        for states in range(dimension):
            statesstr = statesstr + "\"" + str(states + 1) + "\" "
        statesstr = statesstr + "}"
        actsstr = "{ "
        for acts in range(len(players[0])):
            actsstr = actsstr + "\"" + str(acts + 1) + "\" "
        actsstr = actsstr + "}"
        messagesstr = "{ "
        for i in range(dimension):
            messagesstr = messagesstr + "\"" + str(i + 1) + "\" "
        messagesstr = messagesstr + "}"

        # The Players lines
        index = 1
        for states in range(dimension):
            line = "p \"\" 1 " + str(states + 1) + " \"\" " + messagesstr + " 0\n"
            filelist.append(line)
            for i in range(dimension):
                line = "p \"\" 2 " + str(i + 1) + " \"\" " + messagesstr + " 0\n"
                filelist.append(line)
                for acts in range(len(players[states])):
                    line = "t \"\" " + str(index) + " \"\" { " + players[states][acts] + " }\n"
                    filelist.append(line)
                    index = index + 1
        filelist.append("</efgfile>\n</game>\n</gambit:document>")
        stringinput = ''.join(filelist)
        return stringinput

    def calculate_info_content(self, equilibria): # Given Gambit results, calculate in which equilibria do signals carry information
        sinfos = []
        rinfos = []
        jinfos = []
        for line in equilibria:
            mutualinfoSM, mutualinfoAM, mutualinfoSA = self.conditional_probabilities(equilibrium)
            sinfos.append(mutualinfoSM)
            rinfos.append(mutualinfoAM)
            jinfos.append(mutualinfoSA)
        return sinfos, rinfos, jinfos

    def conditional_probabilities(self, equilibrium): # Calculates the
        #conditional probabilities of states on signals, acts on signals, and
        #states of acts
        # Note the resulting matrices have the form: [[P(S1|M1), P(S2|M1), P(S3|M1)], [P(S1|M2), P(S2|M2), P(S3|M2)]...]
        chance = self.chances
        half = int(len(self.payoffs)/2)
        equilibriumsender = equilibrium[:half]
        equilibriumreceiver = equilibrium[half:]
        conditional_probability_matrixsender = []
        unconditionalsmessages = []
        kullbackleibler = []
        for message in range(self.dimension):
            unconditional = sum([chance[i] * equilibriumsender[self.dimension * i + message] for i in range(self.dimension)]) # The unconditional probability of message
            unconditionalsmessages.append(unconditional)
            statesconditionalonmsg = []
            for state in range(self.dimension):
                conditional = chance[state] * safe_div(
                        equilibriumsender[self.dimension * state + message] , unconditional)
                statesconditionalonmsg.append(conditional)

            kld = sum([safe_kld_coefficient(conditional, unconditional) for
                conditional, unconditional in zip(statesconditionalonmsg, chance)])
            kullbackleibler.append(kld)
            conditional_probability_matrixsender.append(statesconditionalonmsg)
        averagekldsender = sum([prob * kbd for prob, kbd in zip(kullbackleibler,
            unconditionalsmessages)])

        jointprobSM = [[conditional_probability_matrixsender[message][state] *
                unconditionalsmessages[message] for state in
                range(self.dimension)] for message in range(self.dimension)]
        mutualinfoSM = sum([jointprobSM[message][state] *
                safe_log(jointprobSM[message][state], self.chances[state] *
                    unconditionalsmessages[message]) for state in
                range(self.dimension) for message in range(self.dimension)])
        ### Then, the information that messages carry about acts ###
        conditional_probability_matrixreceiver= []
        unconditionalsacts = []
        kullbackleibler = []
        # We first calculate the unconditional probability of acts
        for act in range(self.dimension):
            unconditional = sum([unconditionalsmessages[i] *
                equilibriumreceiver[self.dimension * i + act] for i in
                range(self.dimension)]) 
            unconditionalsacts.append(unconditional)
        # Then their probability conditional on a message
        for message in range(self.dimension):
            conditionals4act = []
            if unconditionalsmessages[message] != 0:
                for act in range(self.dimension):
                    conditional = unconditionalsmessages[message] * equilibriumreceiver[self.dimension * message + act] / unconditionalsmessages[message]
                    conditionals4act.append(conditional)
                    #print("act: {}, message: {}, conditional: {}".format(act,
                        #message, conditional))
            else:
                conditionals4act=[0 for i in range(self.dimension)]
            #print("Uncondacts", unconditionalsacts)
            ##print("Cond4acts", conditional)

            kld = sum([safe_kld_coefficient(conditional, unconditional) for
                conditional, unconditional in zip(conditionals4act,
                    unconditionalsacts)])
            kullbackleibler.append(kld)
            #print("KLD: {}".format(kullbackleibler))
            conditional_probability_matrixreceiver.append(conditionals4act)
        averagekldreceiver = sum([prob * kld for prob, kld in zip(
            unconditionalsmessages, kullbackleibler)])

        jointprobAM = [[conditional_probability_matrixreceiver[message][act] *
                unconditionalsmessages[message] for act in
                range(self.dimension)] for message in range(self.dimension)]
        mutualinfoAM = sum([jointprobAM[message][act] *
                safe_log(jointprobAM[message][act], unconditionalsacts[act] *
                    unconditionalsmessages[message]) for act in
                range(self.dimension) for message in range(self.dimension)])
        ### Finally, the info that acts carry about states
        stateconditionalonact = [[safe_div(sum([equilibriumsender[self.dimension * state + message] *
                equilibriumreceiver[self.dimension * message + act] *
                self.chances[state] for message in
                    range(self.dimension)]) , unconditionalsacts[act])
                        for state in range(self.dimension)] for act in
                            range(self.dimension)]
        avgkldjoint = sum([sum([safe_kld_coefficient(stateconditionalonact[act][state], 
            self.chances[state]) for state in
                range(self.dimension)]) * unconditionalsacts[act] for act in
                    range(self.dimension)])
        jointprobSA = [[stateconditionalonact[act][state] *
                unconditionalsacts[act] for state in
                range(self.dimension)] for act in range(self.dimension)]
        mutualinfoSA = sum([jointprobSA[act][state] *
                            safe_log(jointprobSA[act][
                                state], unconditionalsacts[act] * self.chances[
                                    state])
                            for act in range(self.dimension)
                            for state in range(self.dimension)])
        return(mutualinfoSM, mutualinfoAM, mutualinfoSA)


def safe_kld_coefficient(conditional, unconditional):
                if conditional == 0 or unconditional == 0:
                    return 0
                else:
                    return conditional * math.log2(conditional/unconditional)


def safe_log(a, b):
    try:
        return math.log2(safe_div(a, b))
    except ValueError:
        return 0


def safe_div(a, b):
    try:
        return a/b
    except ZeroDivisionError:
        return 0


def payoffs(dimension):  # The payoff matrix, as a list
    return [random.randrange(100) for x in range(dimension*dimension*2)]


def fromlisttomatrix(payoff, dimension):
    # Takes a list of intertwined sender and receiver
    # payoffs (what payoffs() outputs) and outputs two lists of lists.
    sender = [payoff[i] for i in range(0, len(payoff), 2)]
    sendermatrix = [sender[i:i + dimension]
                    for i in range(0, len(sender), dimension)]
    receiver = [payoff[i] for i in range(1, len(payoff), 2)]
    receivermatrix = [receiver[i:i+dimension]
                      for i in range(0, len(receiver), dimension)]
    return sendermatrix, receivermatrix


def preferable(ranking, element1, element2):
    # returns 0 if element1 is
    # preferable; 0.5 if both equally preferable; 1 if element2 is preferable
    index1 = ranking[element1]
    index2 = ranking[element2]
    if index2 > index1:
        return 0
    if index2 == index1:
        return 0.5
    if index2 < index1:
        return 1


def points(state1, state2, element1, element2, tievalue):
    pairwise = abs(preferable(state1, element1, element2)
                   - preferable(state2, element1, element2))
    if pairwise == 0.5:
        return tievalue
    else:
        return pairwise

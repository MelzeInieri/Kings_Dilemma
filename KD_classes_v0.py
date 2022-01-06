# -*- coding: utf-8 -*-
"""
Created on Thu Dec 30 20:59:45 2021

@author: jopwo
"""

import numpy as np

class Player:
    ''' Class for individual players in the endgame of Kings Dilemma'''
    
    # This dictionary links numerical code for tickable boxes to player attributes
    
    def __init__(self, huis = 'noname', prestige = 0, wens = 0, factie = 'pas', ticked = None):
        self.prestige    = prestige
        self.wens        = wens
        self.factie      = factie
        self.huis        = huis
        self.alive       = True
        
        # Dealing with the boxes ticked (or not)
        # 111,112 : defend the gate
        # 121,122 : attack the gate
        # 220     : steal the treasury
        # 312     : help the people
        # 321     : create chaos
        # 322     : protect family
        # 410     : rally populace
        # 511     : message Kasuk
        # 512     : message Kauppias
        # 513     : message Cidlada
        # 611     : protect commander
        # 612     : protect treasure
        # 613     : protect advisor
        # 621     : target commander
        # 622     : target treasurer
        # 623     : target advisor
        self.boxes = {111: False,
                      112: False,
                      121: False,
                      122: False,
                      220: False,
                      311: False,
                      321: False,
                      322: False,
                      410: False,
                      511: False,
                      512: False,
                      513: False,
                      611: False,
                      612: False,
                      613: False,
                      621: False,
                      622: False,
                      623: False}
        if ticked is not None:
            if not np.array_equal(np.asarray(ticked),np.unique(ticked)):
                raise ValueError("variable 'ticked' is not allowed to contain duplicates")
        for t in ticked:
            if t in list(self.boxes.keys()):
                self.boxes[t] = True
            else:
                raise ValueError("box '"+str(t)+"' is invalid Player input")
        self.verdediging = sum([self.boxes[111],self.boxes[112]])
        self.aanval      = sum([self.boxes[121],self.boxes[122]])
    
    @property
    def score(self):
        return self.prestige + self.wens
    
class Game:
    '''Class that runs the endgame of Kings Dilemma given a list of players
    with ticked boxes and starting strengths of light/dark'''
    
    def __init__(self, player_list, strengths = [0,0]):
        self.licht  = strengths[0]
        self.donker = strengths[1]
        self.players = player_list
        
    def run(self):
        
        # Phase 1: the front gate
        self.gate_forces = [0,0]
        for i,p in enumerate(self.players):
            p.prestige           += p.verdediging
            self.gate_forces[0]  += p.verdediging
            p.wens               += p.aanval
            self.gate_forces[1]  += p.aanval
        if self.gate_forces[0] > self.gate_forces[1]:
            self.gate_victory = True
            self.licht       += 40
        elif self.gate_forces[0] < self.gate_forces[1]:
            self.gate_victory = False
            self.donker      += 35
        else:
            self.gate_victory = None
            
        # Phase 2: the treasury
        self.thieves = []
        for i,p in enumerate(self.players):
            if p.boxes[220]:
                self.thieves.append(i)
        if len(self.thieves) != 0:
            treasure = 6//len(self.thieves)
        for i in self.thieves:
            self.players[i].wens += treasure
            
        # Phase 3: house armies
        for i,p in enumerate(self.players):
            if p.boxes[311]:
                p.prestige += 2
                self.licht += 10
            elif p.boxes[321]:
                p.wens     += 1
                self.donker+= 15
            elif p.boxes[322]:
                p.wens     += 3
        
        # Phase 4: rallying the populace
        self.ralliers = []
        for i,p in enumerate(self.players):
            if p.boxes[410]:
                self.ralliers.append(i)
        heroism = 4 - len(self.ralliers)
        for i in self.ralliers:
            self.players[i].prestige += max(heroism,0)
            
        # Phase 5: messengers
        self.allies = {'Kasuk': False, 'Kauppias': False, 'Cidlada': False}
        for i,p in enumerate(self.players):
            if p.boxes[511]:
                self.allies['Kasuk'] = True
            if p.boxes[512]:
                self.allies['Kauppias'] = True
            if p.boxes[513]:
                self.allies['Cidlada'] = True
        if self.allies['Kasuk']:
            self.licht += 25
        if self.allies['Kauppias']:
            self.licht += 20
        if self.allies['Cidlada']:
            self.licht += 15
            
        # Phase 6: assassinations
        self.Opperbevelhebber = {'targeted': False, 'protected': False, 'dead': False}
        self.Schatbewaarder = {'targeted': False, 'protected': False, 'dead': False}
        self.Raadsvrouw = {'targeted': False, 'protected': False, 'dead': False}
        for i,p in enumerate(self.players):
            if p.boxes[611]:
                self.Opperbevelhebber['protected'] = True
                p.prestige += 1
            if p.boxes[612]:
                self.Schatbewaarder['protected'] = True
                p.prestige += 1
            if p.boxes[613]:
                self.Raadsvrouw['protected'] = True
                p.prestige += 1
            if p.boxes[621]:
                self.Opperbevelhebber['targeted'] = True
            if p.boxes[622]:
                self.Schatbewaarder['targeted'] = True
            if p.boxes[623]:
                self.Raadsvrouw['targeted'] = True
        if self.Opperbevelhebber['targeted'] and not self.Opperbevelhebber['protected']:
            self.Opperbevelhebber['dead'] = True
            self.donker += 35
        if self.Schatbewaarder['targeted'] and not self.Schatbewaarder['protected']:
            self.Schatbewaarder['dead'] = True
            self.donker += 30
        if self.Raadsvrouw['targeted'] and not self.Raadsvrouw['protected']:
            self.Raadsvrouw['dead'] = True
            self.donker += 25
            
        # Endphase 1: the battle
        if self.licht > self.donker:
            self.victory = 'licht'
        elif self.licht < self.donker:
            self.victory = 'donker'
        else:
            if self.Raadsvrouw['dead']:
                self.victory = 'donker'
            elif self.Raadsvrouw['dead']:
                self.victory = 'licht'
        
        # Endphase 2: eliminations and battle spoils
        self.survivors = []
        for i,p in enumerate(self.players):
            if p.factie != 'pas':
                if self.victory != p.factie:
                    p.alive = False
                else:
                    self.survivors.append(p)
                    if self.victory == 'licht':
                        p.prestige += 5
                    elif self.victory == 'donker':
                        p.wens     += 5
            else:
                self.survivors.append(p)
        
        # Endphase 3: endgame bonus
        relevant_points = np.zeros(len(self.survivors))
        if self.victory == 'licht':
            for i,s in enumerate(self.survivors):
                relevant_points[i] = s.prestige
            bonus_order = np.flip(np.argsort(relevant_points))
            for j in bonus_order[:3]:
                self.survivors[j].prestige += 5 - 2*j
        if self.victory == 'donker':
            for i,s in enumerate(self.survivors):
                relevant_points[i] = s.wens
            bonus_order = np.flip(np.argsort(relevant_points))
            for j in bonus_order[:3]:
                self.survivors[j].wens += 5 - 2*j
                
        # Endphase 4: The Winner!
        self.winner = None
        self.winning_score = 0
        for i,s in enumerate(self.survivors):
            if s.score > self.winning_score:
                self.winner = s
                self.winning_score = s.score
        
        print("Winnende factie : "+self.victory.capitalize())
        print("Winnaar         : Huize "+self.winner.huis)
        print("Winnende score  : "+str(self.winner.score))
    
        
if __name__ == '__main__':
    
    PP = Player(prestige = 31, wens = 27, huis = 'Piplo-Paplum', ticked = [111, 112], factie = 'licht')
    DA = Player(prestige = 28, wens = 32, huis = 'Duasselak', ticked = [121, 321], factie = 'pas')
    
    Game_test = Game([PP,DA], [50,60])
    Game_test.run()
    

# -*- coding: utf-8 -*-
"""
Created on Thu Dec 30 20:59:45 2021

@author: jopwo
"""

import numpy as np
from enum import Enum

class Actions(Enum):
    DEFEND1  = 0  # : defend the gate
    DEFEND2  = 1 
    ATTACK1  = 2  # : attack the gate
    ATTACK2  = 3
    STEAL    = 4  # : steal the treasury
    PEOPLE   = 5  # : help the people
    CHAOS    = 6  # : create chaos
    FAMILY   = 7  # : protect family
    RALLY    = 8  # : rally populace
    KASUK    = 9  # : message Kasuk
    KAUPPIAS = 10 # : message Kauppias
    CIDLADA  = 11 # : message Cidlada
    PROT_COM = 12 # : protect commander
    PROT_TRE = 13 # : protect treasure
    PROT_ADV = 14 # : protect advisor
    TARG_COM = 15 # : target commander
    TARG_TRE = 16 # : target treasurer
    TARG_ADV = 17 # : target advisor
    
class Factions(Enum):
    LICHT  = 0
    DONKER = 1
    PAS    = 2
    
class Allies(Enum):
    KASUK = 0
    KAUPPIAS = 1
    CIDLADA = 2
    
class Mark:
    ''' Class for the three possible assassination victims in phase 6'''
    
    def __init__(self, targeted = False, unprotected = True, dead = False):
        self.targeted = targeted
        self.unprotected = unprotected
        self.dead = dead

class Player:
    ''' Class for individual players in the endgame of Kings Dilemma'''
    
    def __init__(self, huis = None, prestige = 0, wens = 0, act1 = None, act2 = None, factie = Factions.PAS, plan = None):
        self.prestige    = prestige
        self.wens        = wens
        self.huis        = huis
        self.alive       = True
        self.act1        = act1
        self.act2        = act2
        self.factie      = factie
        self.plan        = plan
        
        # if hasattr(Actions,self.act1.name) and hasattr(Actions,self.act2.name):
        #     if self.act1 == self.act2:
        #         raise ValueError("act1 and act2 are not allowed to be the same")
        # elif not hasattr(Actions,self.act1.name) and self.act1.name is not None:
        #     raise ValueError("act1 is not a valid input (None or Actions enum)")
        # elif not hasattr(Actions,self.act2.name) and self.act2.name is not None:
        #     raise ValueError("act2 is not a valid input (None or Actions enum)")
        # else:
        #     raise ValueError("act1 or act2 are something unexpected...")
          
        # if not hasattr(Factions,self.factie.name) and self.factie.name is not None:
        #     raise ValueError("factie is not a valid input (None or Factions Enum")

        # self.verdediging = sum([self.boxes[111],self.boxes[112]])
        # self.aanval      = sum([self.boxes[121],self.boxes[122]])
    
    @property
    def score(self):
        return self.prestige + self.wens
    
    def choose(self, act1 = None, act2 = None, factie = Factions.PAS, plan = None):
        self.alive       = True
        self.act1        = act1
        self.act2        = act2
        self.factie      = factie
        self.plan        = plan
        
class Piplo_Paplum(Player):
    
    prestige = 31
    wens = 27
    
    def __init__(self, act1 = None, act2 = None, factie = Factions.PAS, plan = None):
        super().__init__(prestige = Piplo_Paplum.prestige, 
                         wens = Piplo_Paplum.wens, 
                         huis = "Piplo-Paplum", 
                         act1 = act1, act2 = act2, factie = factie, plan = plan)
        
    def rechoose(self, act1 = None, act2 = None, factie = Factions.PAS, plan = None):
        self.alive       = True
        self.act1        = act1
        self.act2        = act2
        self.factie      = factie
        self.plan        = plan
        self.prestige = Piplo_Paplum.prestige
        self.wens = Piplo_Paplum.wens
        
class Duasselak(Player):
    
    prestige = 28
    wens = 32
    
    def __init__(self, act1 = None, act2 = None, factie = Factions.PAS, plan = None):
        super().__init__(prestige = Duasselak.prestige, 
                         wens = Duasselak.wens, 
                         huis = "Duasselak", 
                         act1 = act1, act2 = act2, factie = factie, plan = plan)
    
    def rechoose(self, act1 = None, act2 = None, factie = Factions.PAS, plan = None):
        self.alive       = True
        self.act1        = act1
        self.act2        = act2
        self.factie      = factie
        self.plan        = plan
        self.prestige = Duasselak.prestige
        self.wens = Duasselak.wens

class Juppen_van_Jessias(Player):
    
    prestige = 35
    wens = 17
    
    def __init__(self, act1 = None, act2 = None, factie = Factions.PAS, plan = None):
        super().__init__(prestige = Juppen_van_Jessias.prestige, 
                         wens = Juppen_van_Jessias.wens, 
                         huis = "Juppen van Jessias", 
                         act1 = act1, act2 = act2, factie = factie, plan = plan)
        
    def rechoose(self, act1 = None, act2 = None, factie = Factions.PAS, plan = None):
        self.alive       = True
        self.act1        = act1
        self.act2        = act2
        self.factie      = factie
        self.plan        = plan
        self.prestige = Juppen_van_Jessias.prestige
        self.wens = Juppen_van_Jessias.wens
        
class Bonbon_van_Zompestein(Player):
    
    prestige = 51
    wens = 14
    
    def __init__(self, act1 = None, act2 = None, factie = Factions.PAS, plan = None):
        super().__init__(prestige = Bonbon_van_Zompestein.prestige, 
                         wens = Bonbon_van_Zompestein.wens, 
                         huis = "Bonbon van Zompestein", 
                         act1 = act1, act2 = act2, factie = factie, plan = plan)
    
    def rechoose(self, act1 = None, act2 = None, factie = Factions.PAS, plan = None):
        self.alive       = True
        self.act1        = act1
        self.act2        = act2
        self.factie      = factie
        self.plan        = plan
        self.prestige = Bonbon_van_Zompestein.prestige
        self.wens = Bonbon_van_Zompestein.wens
        
class Myrna(Player):
    
    prestige = 12
    wens = 41
    
    def __init__(self, act1 = None, act2 = None, factie = Factions.PAS, plan = None):
        super().__init__(prestige = Myrna.prestige, 
                         wens = Myrna.wens, 
                         huis = "Myrna", 
                         act1 = act1, act2 = act2, factie = factie, plan = plan)

    def rechoose(self, act1 = None, act2 = None, factie = Factions.PAS, plan = None):
        self.alive       = True
        self.act1        = act1
        self.act2        = act2
        self.factie      = factie
        self.plan        = plan
        self.prestige = Myrna.prestige
        self.wens = Myrna.wens
    
class Game:
    '''Class that runs the endgame of Kings Dilemma given a list of players
    with ticked boxes and starting strengths of light/dark'''
    
    def __init__(self, player_list, strengths = [0,0]):
        self.licht   = strengths[0]
        self.donker  = strengths[1]
        self.players = player_list
        self.gate_forces = [0,0]
        self.thieves = []
        self.ralliers = []
        self.allies = {Allies.KASUK: False, Allies.KAUPPIAS: False, Allies.CIDLADA: False}
        self.opperbevelhebber = Mark()
        self.schatbewaarder = Mark()
        self.raadsvrouw = Mark()
        self.resolutions = []
        self.victory = None
        self.survivors = []
        self.survivor_scores = []
        self.winners = []
        self.winning_score = 0
        
    def reset(self, strengths = [0,0]):
        self.licht   = strengths[0]
        self.donker  = strengths[1]
        self.gate_forces = [0,0]
        self.thieves = []
        self.ralliers = []
        self.allies = {Allies.KASUK: False, Allies.KAUPPIAS: False, Allies.CIDLADA: False}
        self.opperbevelhebber = Mark()
        self.schatbewaarder = Mark()
        self.raadsvrouw = Mark()
        self.resolutions = []
        self.victory = None
        self.survivors = []
        self.survivor_scores = []
        self.winners = []
        self.winning_score = 0
        
    def resolve_front_gate(self):
        if self.gate_forces[0] > self.gate_forces[1]:
            self.licht       += 40
        elif self.gate_forces[0] < self.gate_forces[1]:
            self.donker      += 35
            
    def resolve_treasury_theft(self):
        treasure = 6//len(self.thieves)
        for t in self.thieves:
            t.wens += treasure
            
    def resolve_rally(self):
        heroism = 4 - len(self.ralliers)
        for r in self.ralliers:
            r.prestige += max(heroism, 0)
            
    def resolve_kasuk(self):
        self.licht += 25
    def resolve_kauppias(self):
        self.licht += 20
    def resolve_cidlada(self):
        self.licht += 15
            
    def resolve_commander(self):
        if self.opperbevelhebber.unprotected:
            self.opperbevelhebber.dead = True
            self.donker += 35
    def resolve_treasurer(self):
        if self.schatbewaarder.unprotected:
            self.schatbewaarder.dead = True
            self.donker += 30
    def resolve_advisor(self):
        if self.raadsvrouw.unprotected:
            self.raadsvrouw.dead = True
            self.donker += 25
            
    def declare_faction_victory(self):
        if self.licht > self.donker:
            self.victory = Factions.LICHT
        elif self.licht < self.donker:
            self.victory = Factions.DONKER
        else:
            if self.raadsvrouw.dead:
                self.victory = Factions.DONKER
            else:
                self.victory = Factions.LICHT
                
    def award_spoils(self):
        for p in self.players:
            if p.factie != Factions.PAS:
                if self.victory != p.factie:
                    p.alive = False
                else:
                    self.survivors.append(p)
                    if self.victory == Factions.LICHT:
                        p.prestige += 5
                    elif self.victory == Factions.DONKER:
                        p.wens     += 5
            else:
                self.survivors.append(p)
                
    def award_endgame_bonus(self):
        player_points = np.zeros(len(self.survivors))
        if self.victory == Factions.LICHT:
            for i,s in enumerate(self.survivors):
                player_points[i] = s.prestige
            unique_points = np.flip(np.unique(np.sort(player_points)))
            for j,m in enumerate(unique_points[:3]):
                for s in self.survivors:
                    if s.prestige == m:
                        s.prestige += 5 - 2*j
        if self.victory == Factions.DONKER:
            for i,s in enumerate(self.survivors):
                player_points[i] = s.wens
            unique_points = np.flip(np.unique(np.sort(player_points)))
            for j,m in enumerate(unique_points[:3]):
                for s in self.survivors:
                    if s.wens == m:
                        s.wens += 5 - 2*j
                
    def declare_winners(self):
        for s1 in self.survivors:
            self.survivor_scores.append(s1.score)
        if len(self.survivor_scores) != 0:
            self.winning_score = max(self.survivor_scores)
        for s2 in self.survivors:
            if s2.score == self.winning_score:
                self.winners.append(s2)
        # print("Winnende factie : "+self.victory.name.capitalize())
        # print("Winnaar         : Huize ",self.winners)
        # print("Winnende score  : "+str(self.winning_score))
    
        
    def defend(self, player):
        self.gate_forces[0] += 1
        player.prestige += 1
        self.resolutions.append(self.resolve_front_gate)
        
    def attack(self, player):
        self.gate_forces[1] += 1
        player.wens += 1
        self.resolutions.append(self.resolve_front_gate)
    
    def steal(self, player):
        self.thieves.append(player)
        self.resolutions.append(self.resolve_treasury_theft)
        
    def help_people(self, player):
        self.licht += 10
        player.prestige += 2
        
    def create_chaos(self, player):
        self.donker += 15
        player.wens += 1
        
    def protect_family(self, player):
        player.wens += 3
    
    def rally(self, player):
        self.ralliers.append(player)
        self.resolutions.append(self.resolve_rally)
    
    def message_kasuk(self, player):
        self.allies[Allies.KASUK] = True
        self.resolutions.append(self.resolve_kasuk)
    def message_kauppias(self, player):
        self.allies[Allies.KAUPPIAS] = True
        self.resolutions.append(self.resolve_kauppias)
    def message_cidlada(self, player):
        self.allies[Allies.CIDLADA] = True
        self.resolutions.append(self.resolve_cidlada)
    
    def target_opperbevelhebber(self, player):
        self.opperbevelhebber.targeted = True
        self.resolutions.append(self.resolve_commander)
    def target_schatbewaarder(self, player):
        self.schatbewaarder.targeted = True
        self.resolutions.append(self.resolve_treasurer)
    def target_raadsvrouw(self, player):
        self.raadsvrouw.targeted = True
        self.resolutions.append(self.resolve_advisor)
        
    def protect_opperbevelhebber(self, player):
        self.opperbevelhebber.unprotected = False
        player.prestige += 1
    def protect_schatbewaarder(self, player):
        self.schatbewaarder.unprotected = False
        player.prestige += 1
    def protect_raadsvrouw(self, player):
        self.raadsvrouw.unprotected = False
        player.prestige += 1
        
    actionlib = {Actions.DEFEND1: defend,
                 Actions.DEFEND2: defend,
                 Actions.ATTACK1: attack,
                 Actions.ATTACK2: attack,
                 Actions.STEAL: steal,
                 Actions.PEOPLE: help_people,
                 Actions.CHAOS: create_chaos,
                 Actions.FAMILY: protect_family,
                 Actions.RALLY: rally,
                 Actions.KASUK: message_kasuk,
                 Actions.KAUPPIAS: message_kauppias,
                 Actions.CIDLADA: message_cidlada,
                 Actions.PROT_COM: protect_opperbevelhebber,
                 Actions.PROT_TRE: protect_schatbewaarder,
                 Actions.PROT_ADV: protect_raadsvrouw,
                 Actions.TARG_COM: target_opperbevelhebber,
                 Actions.TARG_TRE: target_schatbewaarder,
                 Actions.TARG_ADV: target_raadsvrouw}
    
    def perform_actions(self, actionlib = actionlib):
        '''The action library will do all instaneous actions and flag things
        that need to be resolved after the for loop. Flagging happens by adding
        the relevant functions to the self.resolutions list (which later gets
        cropped to its unique members)'''
        for p in self.players:
            actionlib[p.act1](self, p)
            actionlib[p.act2](self, p)
            
    def run(self, actionlib = actionlib):
        ''' this is the main method, running the game from input to winner'''
        
        # Step 1: perform instantaneous actions, add resolution functions to
        # self.resolutions as necessary
        self.perform_actions(actionlib = actionlib)
        
        # Step 2: crop list of resolutions to set of unique entries, 
        # then perform them
        self.resolutions = set(self.resolutions)
        for f in self.resolutions:
            f()
            
        # Step 3: declare winning faction, eliminate or add bonus points accordingly 
        self.declare_faction_victory()
        self.award_spoils()
        self.award_endgame_bonus()
        
        # Step 4: declare the winner!
        self.declare_winners()
        
    
        
if __name__ == '__main__':
    
    PP = Piplo_Paplum(act1 = Actions.DEFEND1, 
                      act2 = Actions.RALLY, 
                      factie = Factions.LICHT)
    DA = Duasselak(act1 = Actions.ATTACK1, 
                   act2 = Actions.CHAOS, 
                   factie = Factions.DONKER)
    
    Game_test = Game([PP,DA], [50,60])
    Game_test.run()
    

# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 14:26:24 2022

@author: jopwo
"""

import KD_classes as KDC
import time

def players_init():
    ''' Single, somewhat realistic player initialisation of Kings Dilemma for testing purposes'''
    
    PP = KDC.Piplo_Paplum(act1 = KDC.Actions.DEFEND1, 
                          act2 = KDC.Actions.RALLY, 
                          factie = KDC.Factions.LICHT)
    DA = KDC.Duasselak(act1 = KDC.Actions.ATTACK1, 
                       act2 = KDC.Actions.CHAOS, 
                       factie = KDC.Factions.DONKER)
    JJ = KDC.Juppen_van_Jessias(act1 = KDC.Actions.DEFEND1,
                                act2 = KDC.Actions.KASUK, 
                                factie = KDC.Factions.LICHT)
    BZ = KDC.Bonbon_van_Zompestein(act1 = KDC.Actions.KASUK, 
                                   act2 = KDC.Actions.PROT_ADV, 
                                   factie = KDC.Factions.PAS)
    MY = KDC.Myrna(act1 = KDC.Actions.STEAL, 
                   act2 = KDC.Actions.RALLY, 
                   factie = KDC.Factions.DONKER)
    
    return PP, DA, JJ, BZ, MY

def players_choose(PP, DA, JJ, BZ, MY):
    ''' Single, somewhat realistic player RE-initialisation of Kings Dilemma for testing purposes'''
    
    PP.rechoose(act1 = KDC.Actions.DEFEND1, 
                act2 = KDC.Actions.RALLY, 
                factie = KDC.Factions.LICHT)
    DA.rechoose(act1 = KDC.Actions.ATTACK1, 
                act2 = KDC.Actions.CHAOS, 
                factie = KDC.Factions.DONKER)
    JJ.rechoose(act1 = KDC.Actions.DEFEND1,
                act2 = KDC.Actions.KASUK, 
                factie = KDC.Factions.LICHT)
    BZ.rechoose(act1 = KDC.Actions.KASUK, 
                act2 = KDC.Actions.PROT_ADV, 
                factie = KDC.Factions.PAS)
    MY.rechoose(act1 = KDC.Actions.STEAL, 
                act2 = KDC.Actions.RALLY, 
                factie = KDC.Factions.DONKER)

if __name__ == '__main__':
    
    n = 100000
    t0 = time.perf_counter()
    PP, DA, JJ, BZ, MY = players_init()
    mygame = KDC.Game([PP,DA,JJ,BZ,MY],[50,60])
    for i in range(n):
        players_choose(PP,DA,JJ,BZ,MY)
        # mygame = KDC.Game([PP,DA,JJ,BZ,MY],[50,60])
        mygame.reset([50,60])
        mygame.run()
        if i%10000 == 0:
            print(mygame.winning_score)
    t1 = time.perf_counter()
    print(str(t1-t0))
    
    # PP,DA,JJ,BZ,MY = players_init()
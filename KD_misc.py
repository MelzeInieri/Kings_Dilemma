# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 15:17:48 2022

@author: jopwo
"""

import numpy as np

import KD_batchrunning as KDB
import KD_classes as KDC

def summarise_game_instance(players, planlist, data_full_row, verbose = False):
    
    summ_dict = {}
    for i,p in enumerate(players):
        plan = plan_single_to_strings(data_full_row[i], planlist)
        summ_dict.update({p.huis: plan})
        
    if verbose:
        print(summ_dict)
        
    return summ_dict

def plan_single_to_triplet(plan, planlist):
    
    plan_full = [0, [0,0]]
    plan_full[0] = planlist[plan][0]
    plan_full[1][0] = planlist[plan][1][0]
    plan_full[1][1] = planlist[plan][1][1]
    
    return plan_full
    
def plan_single_to_strings(plan, planlist):
    
    plan_full = [0, [0,0]]
    plan_full[0] = KDC.Factions(planlist[plan][0]).name
    plan_full[1][0] = KDC.Actions(planlist[plan][1][0]).name
    plan_full[1][1] = KDC.Actions(planlist[plan][1][1]).name
    
    return plan_full

def game_from_plans(plans,planlist):
    
    BZ,DA,PP,MY,JJ = KDB.players_init()
    players = [BZ,DA,PP,MY,JJ]
    
    for i,p in enumerate(players):
        p.rechoose(act1 = KDC.Actions(planlist[plans[i]][1][0]),
                   act2 = KDC.Actions(planlist[plans[i]][1][1]),
                   factie = KDC.Factions(planlist[plans[i]][0]),
                   plan = plans[i])
        
    mygame = KDC.Game(players, strengths = [50,60])
    mygame.reset(strengths = [50,60])
    mygame.run()
    
    return mygame

def nowinners_check(players, planlist, data_full):
    
    
    X = np.sum(data_full[:,0] == 9)
    
    if X > 0:
        print("There are ",X," cases with no winners!")
        nowinners_data = data_full[np.nonzero(data_full[:,0] == 9)][0]
        print("data_full entry: ", np.nonzero(data_full[:,0] == 9)[0])
        summ_dict = summarise_game_instance(players,planlist, nowinners_data[1:], verbose = True)
        summ_dict.update({'nowinners_plans': nowinners_data.copy()})
    else:
        summ_dict = None
        
    return summ_dict
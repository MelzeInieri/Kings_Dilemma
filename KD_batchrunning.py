# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 15:13:59 2022

@author: jopwo
"""

import time
from datetime import datetime
import pickle
import numpy as np

import KD_classes as KDC

def get_datetimestring():
    
    now = datetime.now()
    
    year = datetime.strftime(now, '%Y')[2:]
    
    datetimestring = year+datetime.strftime(now, '%m%d_%H%M')
    
    return datetimestring

def read_from_file(filename):
    
    with open(filename, 'rb') as infile:
        data = pickle.load(infile)
        
    return data

def write_to_file(data, filename = None):
    
    if filename is None:
        filename = get_datetimestring()+'.pickle'
    
    with open(filename, 'wb') as outfile:
        pickle.dump(data, outfile)

def players_init():
    ''' Single, somewhat realistic player initialisation of Kings Dilemma for testing purposes'''
    
    BZ = KDC.Bonbon_van_Zompestein(act1 = KDC.Actions.KASUK, 
                                   act2 = KDC.Actions.PROT_ADV, 
                                   factie = KDC.Factions.PAS)
    DA = KDC.Duasselak(act1 = KDC.Actions.ATTACK1, 
                       act2 = KDC.Actions.CHAOS, 
                       factie = KDC.Factions.DONKER)
    PP = KDC.Piplo_Paplum(act1 = KDC.Actions.DEFEND1, 
                          act2 = KDC.Actions.RALLY, 
                          factie = KDC.Factions.LICHT)
    MY = KDC.Myrna(act1 = KDC.Actions.STEAL, 
                   act2 = KDC.Actions.RALLY, 
                   factie = KDC.Factions.DONKER)
    JJ = KDC.Juppen_van_Jessias(act1 = KDC.Actions.DEFEND1,
                                act2 = KDC.Actions.KASUK, 
                                factie = KDC.Factions.LICHT)
    
    return BZ, DA, PP, MY, JJ

def players_choose(players, planlist, diceroller, choice_weights = None):
    
    M = len(planlist)
    
    if choice_weights == None:
        for p in players:
            plan = diceroller.choice(M)
            p.rechoose(act1 = KDC.Actions(planlist[plan][1][0]),
                       act2 = KDC.Actions(planlist[plan][1][1]),
                       factie = KDC.Factions(planlist[plan][0]),
                       plan = plan)
    
def simulate_N_games(N, players, planlist, diceroller, choice_weight = None, save_data_full = False):
    
    M = len(planlist)
    
    data_stat = np.zeros((5,M,2), dtype = int)
    if save_data_full:
        data_full = 9*np.ones((N,6), dtype = int)
    else:
        data_full = None
        
    TheGame = KDC.Game(players,[50,60])
    for i in range(N):
        players_choose(players, planlist, diceroller)
        TheGame.reset([50,60])
        TheGame.run()
        for j,p in enumerate(players):
            data_stat[j,p.plan,0] += 1
            if save_data_full:
                data_full[i,j+1] = p.plan
            if p in TheGame.winners:
                data_stat[j,p.plan,1] += 1
                if save_data_full:
                    if data_full[i,0] == 9:
                        data_full[i,0] = j
                    else:
                        data_full[i,0] = data_full[i,0]+10**j*j
        # if data_full[i,0] == 9:
        #     print(TheGame.winners)
        #     for p in players:
        #         print(p in TheGame.winners)
        #     break
                
    return data_stat, data_full, TheGame

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
    
    BZ,DA,PP,MY,JJ = players_init()
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

def get_new_batch(planlist_filename, N = 1000):
    
    planlist = read_from_file(planlist_filename)
    BZ,DA,PP,MY,JJ = players_init()
    players = [BZ,DA,PP,MY,JJ]
    diceroller = np.random.default_rng()
    
    tic = time.perf_counter()
    data_stat, data_full, game_last = simulate_N_games(N, players, planlist, diceroller = diceroller, save_data_full = True)
    toc = time.perf_counter()
    print("Duration: ",toc-tic, " seconds")
    
    return planlist, players, data_stat, data_full, game_last

if __name__ == '__main__':

    planlist, players, data_stat, data_full, game_last = get_new_batch('planlist_strong_1.pickle', N = 1000000)
    
    write_to_file(data_stat, 'strong_1_stat_01.pickle')

    # nowinners_summ_dict = nowinners_check(players, planlist, data_full)
    # nowinners_game = game_from_plans(nowinners_summ_dict['nowinners_plans'], planlist)
    
    
    
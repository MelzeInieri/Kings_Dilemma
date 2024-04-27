# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 15:13:59 2022

@author: jopwo
"""

import time
import numpy as np

import KD_classes as KDC
import filetools as ft

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
    
    if choice_weights is None:
        for p in players:
            plan = diceroller.choice(M)
            p.rechoose(act1 = KDC.Actions(planlist[plan][1][0]),
                       act2 = KDC.Actions(planlist[plan][1][1]),
                       factie = KDC.Factions(planlist[plan][0]),
                       plan = plan)
    else:
        for i,p in enumerate(players):
            plan = diceroller.choice(M, p = choice_weights[i,:])
            p.rechoose(act1 = KDC.Actions(planlist[plan][1][0]),
                       act2 = KDC.Actions(planlist[plan][1][1]),
                       factie = KDC.Factions(planlist[plan][0]),
                       plan = plan)
    
def simulate_N_games(N, players, planlist, diceroller, choice_weights = None, save_data_full = False):
    
    P = len(players)
    
    M = len(planlist)
    if choice_weights is not None:
        if np.size(choice_weights,1) != M:
            raise ValueError("choice weights are not of equal length to planlist")
        else:
            choice_weights_copy = choice_weights.copy().astype(float)
            for i in range(np.size(choice_weights,0)):
                choice_weights_copy[i,:] = choice_weights[i,:]/np.linalg.norm(choice_weights[i,:],1)
    else:
        choice_weights_copy = None
    
    # data_stat: [player, plan ID, [total, 1st place, 2nd place, etc]]
    data_stat = np.zeros((P,M,7), dtype = int)
    if save_data_full:
        # data_full: [game ID, player, [place, plan]]
        data_full = np.ones((N,P,2), dtype = int)
    else:
        data_full = None
        
    TheGame = KDC.Game(players,[50,60])
    for i in range(N):
        players_choose(players, planlist, diceroller, choice_weights_copy)
        TheGame.reset([50,60])
        TheGame.run()
        for j,p in enumerate(players):
            data_stat[j,p.plan,0]       += 1
            data_stat[j,p.plan,p.place] += 1
            if save_data_full:
                # data_full[i,j+1] = p.plan
                data_full[i,j,0] = p.place
                data_full[i,j,1] = p.plan
                
    return data_stat, data_full, TheGame

def score_plan_performance(batchdata, scoring = "win_lose", exp_base = 2):
    '''
    Gives a score to the performance of a plan given the ranks achieved with it
    scaled by its occurrence, per player. Multiple schemes are available. 
    E.g. exponential rank_scoring with an exp_base of 2 means coming 2nd 
    is worth 2^4 = 16 points with 5 players.
    '''
    
    N_players, N_plans, N_ranks = batchdata.shape
    N_ranks -= 1 # first block there is total games, not a rank
    
    plan_score_rates = np.zeros((N_players, N_plans))
    if scoring == 'exponential':
        for p in range(N_players):
            for i in range(N_plans):
                plan_score = 0
                for j in range(1,N_ranks+1):
                    plan_score += batchdata[p,i,j]*exp_base**(N_ranks - j)
                plan_score_rates[p,i] = plan_score/batchdata[p,i,0]
    elif scoring == 'win_lose':
        for p in range(N_players):
            plan_score_rates[p,:] = batchdata[p,:,1]/batchdata[p,:,0]
    else:
        raise ValueError("scoring requested does not match available options")
    
    return plan_score_rates

def get_new_batch(planlist_filename, N = 1000, choice_weights = None, save_data_full = True):
    
    planlist = ft.read_file(planlist_filename)
    BZ,DA,PP,MY,JJ = players_init()
    players = [BZ,DA,PP,MY,JJ]
    diceroller = np.random.default_rng()
    
    tic = time.perf_counter()
    data_stat, data_full, game_last = simulate_N_games(N, players, planlist, diceroller = diceroller, 
                                                       choice_weights = choice_weights, 
                                                       save_data_full = save_data_full)
    toc = time.perf_counter()
    print("Duration: ",toc-tic, " seconds")
    
    return data_stat, data_full, (planlist, players, game_last)

if __name__ == '__main__':

    data_stat, data_full, (planlist, players, game_last) = get_new_batch('planlist_strong_1.pickle', N = 100000)
    
    # write_to_file(data_stat, 'strong_1_stat_01.pickle')

    # nowinners_summ_dict = nowinners_check(players, planlist, data_full)
    # nowinners_game = game_from_plans(nowinners_summ_dict['nowinners_plans'], planlist)
    
    pass
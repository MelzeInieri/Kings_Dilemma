# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 19:29:36 2022

@author: jopwo
"""

import numpy as np
import os

import KD_batchrunning as KDB
import filetools as ft

def adjust_weights(weights_in, batchdata,
                   rank_scoring = 'exponential',
                   exp_base = 2,
                   adjustment_fraction = 0.5, 
                   minimum_weight = 0.005):
    '''
    adjusts the probabilities of players to choose specific strategies based
    on their relative scoring with those same strategies. The adjustment fraction
    stipulates the extent the weights are adjusted. An adjustment_fraction of x
    means the new weight will be (1-x) + x*relative_winrate (0 to 1).
    Afterwards the weights are renormalised.
    minimum_weight is the fraction of the hypothetical uniform weight the actual
    weights will be set at if they fall below it.
    Scoring is based on the ranks players achieved with a particular plan,
    and multiple schemes are available. E.g., exponential rank_scoring with
    an exp_base of 2 means coming 2nd is worth 2^4 = 16 points with 5 players.
    '''
    
    N_players, N_plans, N_ranks = batchdata.shape
    
    weights_out = weights_in.copy().astype(float)
    
    # Determining the scoring rates that will adjust the weights
    plan_score_rates = KDB.score_plan_performance(batchdata, rank_scoring, exp_base)
    # The actual adjusting
    for p in range(N_players):
        plan_score_rates_rangenormed = plan_score_rates[p,:]/np.max(plan_score_rates[p,:])
        weights_out[p,:] = weights_out[p,:]*((1-adjustment_fraction)+adjustment_fraction*plan_score_rates_rangenormed)
        weights_out[p,:] = weights_out[p,:]/np.linalg.norm(weights_out[p,:],1)
        for i,w in enumerate(weights_out[p,:]):
            if w < minimum_weight/N_plans:
                weights_out[p,i] = minimum_weight/N_plans
        weights_out[p,:] = weights_out[p,:]/np.linalg.norm(weights_out[p,:],1)    
    
    return weights_out

def iterate_batches(batchdatafile_in, planfile = 'planlist_strong_1.pickle',
                    K = 1, N = 100000, 
                    scoring = 'exponential', exp_base = 2, 
                    adjustment_fraction = 0.25, minimum_weight = 0.005,
                    write_last = True, write_all = False,
                    fileout = None, new_branch = False):
    
    if batchdatafile_in is not None and os.path.isfile(batchdatafile_in):
        batchdata = ft.read_file(batchdatafile_in)['batchdata'].copy()
    else:
        batchdata = None
        N_P = len(ft.read_file(planfile))
        weights = np.ones((5,N_P))/N_P
        
    if fileout == None:
        fileout = batchdatafile_in
    
    save_data_full = False
    # batchdata = batchdata_in.copy()
    for i in range(K):
        
        if batchdata is not None:
            weights = adjust_weights(batchdata[:,:,0], batchdata, 
                                     adjustment_fraction = adjustment_fraction,
                                     minimum_weight = minimum_weight)
        if i == K-1:
            save_data_full = True
        
        batchdata, batchstrats, (planlist, players, game_last) = KDB.get_new_batch(planfile, N, choice_weights = weights, save_data_full = save_data_full)
        
        
        if write_all or (write_last and i == K-1):
            savedict = {'batchdata': batchdata,
                        'planfile': planfile,
                        'batchstrats': batchstrats,
                        'scoring': scoring,
                        'exp_base': exp_base,
                        'adjustment_fraction': adjustment_fraction,
                        'parentbatch': batchdatafile_in,
                        'N': N,
                        'K': K}
            
            fileout = ft.increment_filename(fileout)
            ft.write_file(savedict, fileout)
            
    return batchdata, batchstrats, (planlist, players, game_last)

if __name__ == '__main__':
    
    # data = ft.read_file('strong_1_stat_01.pickle')
    # weights_uniform = np.ones((5,10))
    # weights_test = adjust_weights(weights_in = weights_uniform, batchdata = data[:,50:60,:],
    #                               rank_scoring = 'win_lose')
    # print(np.max(weights_test,1))
    # print(np.min(weights_test,1))
    # print(np.average(weights_test,1))
    
    # datafile_in = 'strong_1_stat_01.pickle'
    planfile = 'plans35.pickle'
    fileout = 'Batchseries/set35'
    batchdata, batchstrats, (planlist, players, game_last) = iterate_batches(None,
                                                                           planfile,
                                                                           K = 15, N = 1000000,
                                                                           adjustment_fraction = 0.5,
                                                                           write_all = True,
                                                                           write_last = True,
                                                                           fileout = fileout)
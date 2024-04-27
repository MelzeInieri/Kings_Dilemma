# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 20:23:48 2022

@author: jopwo
"""

# import time
from datetime import datetime
import pickle
import numpy as np

import matplotlib.pyplot as plt

import KD_batchrunning as KDB
import KD_evolution as KDE
import filetools as ft
import statistictools as st

def player_plot(data, player, ylim = True):
    plt.figure(dpi=600)
    ax = plt.axes()
    
    N = np.size(data,1)
    
    win_fractions = np.zeros(N)
    for i in range(N):
        win_fractions[i] = data[player,i,1]/data[player,i,0]
        
    ax.plot(win_fractions)
    ax.set_title("Player "+str(player))
    ax.set_ylabel("win fraction of plan")
    if ylim:
        ax.set_ylim([0,1])
    
    plt.tight_layout()
    plt.show()
    
def evolve_strategies(N, planfile, winfile_in, adjustment_fraction = 0.25, minimum_weight = 0.005, winfile_out = True, show_plot = True):
    '''
    A single iteration of playing N games with weighted plan choices.
    The input is a windata file of a previous run with the same planlist.
    The choice weights are based on the outcome of that run, based on the 
    adjustment_fraction (see adjust_weights in KD_batchrunning)
    The plot shown, if not deactivated, has the previous iteration on the left side
    and the new iteration on the right. 
    Top is relative choice occurrence / weights, bottom is relative winrate.
    The new windata are written to a file that, if file_out is a True instead of
    a string, is based on the old filename.
    '''
    
    windata_in = ft.read_file(winfile_in)
    weights_adjusted = KDB.adjust_weights(windata_in[:,:,0], windata_in, adjustment_fraction, minimum_weight)
    
    planlist, players, windata_out, stratdata_out, game_last = KDB.get_new_batch(planfile, N, choice_weights = weights_adjusted)
    
    if show_plot:
        plot_strategy_evolution(windata_in, windata_out)
        
    return planlist, players, windata_in, windata_out, stratdata_out, game_last

def inverse_turfdict(batchdata, N, mode = 'worst'):
    
    sort_idx = np.argsort(batchdata[:,:,0],1)
    if mode == 'worst':
        turfdict = st.turfdict(sort_idx[:,:N])
    elif mode == 'best':
        turfdict = st.turfdict(sort_idx[:,-N:])
    turfinv = st.dict_inversion(turfdict)
    
    for key in turfinv:
        turfinv[key].sort()
    
    return turfinv

def plot_strategy_evolution(batchdata_in, batchdata_out,
                            scoring = 'win_lose',
                            exp_base = 2):
    '''
    The plot has the old batch on the left side
    and the new iteration on the right. 
    Top is relative choice occurrence / weights, bottom is relative winrate.
    '''
    
    P = np.size(batchdata_in,0) # index of player
    if P != np.size(batchdata_out,0):
        raise ValueError("data are not of the same amount of players")
    
    weights_in = batchdata_in[:,:,0].copy().astype(float)
    weights_out = batchdata_out[:,:,0].copy().astype(float)
    for p in range(P):
        weights_in[p,:] = weights_in[p,:]/np.max(weights_in[p,:])
        weights_out[p,:] = weights_out[p,:]/np.max(weights_out[p,:])
    
    # scores_in = batchdata_in[:,:,1]/batchdata_in[:,:,0]
    # scores_out = batchdata_out[:,:,1]/batchdata_out[:,:,0]
    
    scores_in = KDB.score_plan_performance(batchdata_in, scoring = scoring, exp_base = 2)
    scores_out = KDB.score_plan_performance(batchdata_out, scoring = scoring, exp_base = 2)
    
    fig = plt.figure(dpi = 600)
    ax_in_weights = fig.add_subplot(221)
    ax_in_winrate = fig.add_subplot(223)
    ax_out_weights = fig.add_subplot(222)
    ax_out_winrate = fig.add_subplot(224)
    
    ax_in_weights.set_title("Old run")
    ax_in_weights.set_ylabel("relative occurrence/weights")
    ax_in_winrate.set_ylabel("plan performance")
    ax_in_winrate.set_xlabel("plan index")
    
    ax_out_weights.set_title("New run")

    ax_out_winrate.set_xlabel("plan index")
    
    ax_in_weights.set_ylim([0,1])
    # ax_in_winrate.set_ylim([0,1])
    ax_out_weights.set_ylim([0,1])
    # ax_out_winrate.set_ylim([0,1])
    
    ax_in_weights.plot(weights_in.T, linewidth = 0.5)
    ax_in_winrate.plot(scores_in.T, linewidth = 0.5)
    ax_out_weights.plot(weights_out.T, linewidth = 0.5)
    ax_out_winrate.plot(scores_out.T, linewidth = 0.5)
    
    plt.tight_layout()
    plt.show
    
    return
    
def plot_single(batchdata_in):
    
    P = np.size(batchdata_in,1)
    
    fig = plt.figure(dpi = 600)
    ax = plt.axes()
    
    ax.plot(batchdata_in[:,:,0].T, linewidth = 0.25)
    
    plt.xticks(np.arange(0,P,10))
    plt.tight_layout()
    plt.show()
    
    return

def performance_summary(playerid, batchdata, scoring, planlist):
    
    summary = []
    for faction in [0,1,2]:
        planidxs = [i for i in range(len(planlist)) if planlist[i][0] == faction]
        subset = batchdata[:, planidxs, :]
        subset_scores = KDB.score_plan_performance(subset, scoring = scoring, exp_base = 2)[playerid,:]
        subset_score_sort = np.flip(np.argsort(subset_scores))
        for rank in range(5):
            summary.append([planlist[planidxs[subset_score_sort[rank]]],
                            planidxs[subset_score_sort[rank]],
                            subset[playerid, subset_score_sort[rank],0],
                            np.around(subset_scores[subset_score_sort[rank]],1)])
    
    summary = np.asarray(summary, dtype = object)
    return summary

if __name__ == '__main__':
    
    # planlist, players, windata_in, windata_out, stratdata_out, game_last = evolve_strategies(100000, 
    #                                                                                          planfile = 'planlist_strong_1.pickle', 
    #                                                                                          winfile_in = 'strong_1_stat_01.pickle',
    #                                                                                          adjustment_fraction = 0.5,
    #                                                                                          show_plot = False)
    
    planlist = ft.read_file('plans35.pickle')
    batch1 = ft.read_file("Batchseries/set35_01.pickle")
    batch2 = ft.read_file("Batchseries/set35_10.pickle")
    
    data1  = batch1['batchdata']
    data2  = batch2['batchdata']
    scoring = batch2['scoring']
    
    plot_strategy_evolution(data1, data2, scoring)
    # plot_single(data2)
    # JJ = performance_summary(4, data2, scoring, planlist)
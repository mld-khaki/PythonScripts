# -*- coding: utf-8 -*-
# mld_aux_lib

import numpy as np
import pandas as pd

def max_interval(spk_times):
    #Burst parameters
    MAX_BEGIN_ISI = 0.17  # 0.17
    MAX_END_ISI = 0.3  # 0.3
    MIN_IBI = 0.2
    MIN_brst_dur = 0.01
    MIN_SPIKES_IN_BURST = 4

    spk_num = len(spk_times)

    in_brst = False
    brst_num = 0
    brst_cur = []
    allBursts = []

    '''
    Phase 1: Burst Detection
    Here a burst is defined as starting when two consecutive spikes have an ISI less than MAX_BEGIN_ISI. The end of the
    burst is given when two spikes have an ISI greater than MAX_END_ISI.
    Find ISIs closer than MAX_BEGIN_ISI and end with MAX_END_ISI.
    The last spike of the previous burst will be used to calculate the IBI.
    For the first burst, there is no previous IBI.
    '''
    n = 2

    while (n < spk_num):
        ISI = spk_times[n] - spk_times[n-1]  # Calculate ISI
        if in_brst == True:  # currently in burst
            if ISI > MAX_END_ISI:  # end the burst if ISI is greater than the END threshold
                brst_cur.append(spk_times[n-1])  # Store last spike in burst
                brst_num += 1
                allBursts.append(brst_cur)  # Store burst data
                brst_cur = []  # Reset current burst
                in_brst = False
            else:
                brst_cur.append(spk_times[n-1])
        else:  # currently not in burst
            if ISI < MAX_BEGIN_ISI:  # possible found start of new burst
                brst_cur.append(spk_times[n-1])
                in_brst = True
        n += 1

    # Calculate IBIs
    IBI = []
    for bCtr in range(1, brst_num):
        prevBurstEnd = allBursts[bCtr-1][-1]
        currBurstBeg = allBursts[bCtr][0]
        IBI.append(currBurstBeg - prevBurstEnd)

    '''
    Phase 2: Merging of bursts_ar
    Here we see if any pair of bursts_ar have an IBI less than MIN_IBI; if so, we then merge the bursts. We specifically
    need to check when say three bursts are merged into one
    '''

    tmp = allBursts
    allBursts = []
    for b in range(1, brst_num):
        prevBurst = tmp[b-1]
        currBurst = tmp[b]
        if IBI[b-1] < MIN_IBI:  # IBI is too short to be separate bursts
            prevBurst = np.hstack((prevBurst, currBurst))
        allBursts.append(prevBurst)
    if brst_num >= 2:
        allBursts.append(currBurst)

    '''
    Phase 3: Quality Control
    Remove small bursts less than min_bursts_duration or having too few spikes less than min_spikes_in_bursts. In this 
    phase we have the possibility of deleting all spikes.
    '''
    tooShort = 0
    if brst_num > 1:
        for b in range(0,brst_num):
            brst_cur = allBursts[b]
            if len(brst_cur) < MIN_SPIKES_IN_BURST:
                brst_cur = []
            elif (brst_cur[-1] - brst_cur[0]) < MIN_brst_dur:
                brst_cur = []
                tooShort += 1
            allBursts[b] = brst_cur

    #tooShort = tooShort/len(allBursts)

   #all_brst_final = [x for x in allBursts if x]

    all_brst_final = []
    for x in allBursts:
        #print(np.array(x).size)
        if np.array(x).size != 0:
          all_brst_final.append(x)

    return all_brst_final


def get_brst_dur(burst):
    return (burst[-1] - burst[0])


def get_brst_isi(burst):
    return (np.mean(np.diff(burst)))


def get_ibi(brst_ar):
    ibi = []
    for i in range(len(brst_ar) - 1):
        first_brst = brst_ar[i]
        second_brst = brst_ar[i + 1]
        interval = second_brst[0] - first_brst[-1]
        ibi.append(interval)
    return ibi

def get_feature_template():
    DFs = {'Well':[''], 'Plate': 0,
                  'Week': 3,    'x_ele':0,      'y_ele':0,      'elect':0,
                  'amp_avg':0,  'amp_std':0,    'max_int':0,    'spk_num':0,
                  'isi':0,      'isi_std':0,    'isi_cv':0,
                  'brst_num':0, 'spk_num_brst':0,               'spk_num_brst_std':0,
                  'spk_num_brst_cv':0,          'spk_num_non_brst':0, 
                  'brst_dur':0, 'brst_dur_std':0,               'brst_dur_cv':0, 
                  'brst_isi':0, 'brst_isi_std':0,               'brst_isi_cv':0, 
                  'ibi':0,      'ibi_std':0,    'ibi_cv':0}
    return pd.DataFrame(DFs)
def extract_features(spk_times,DFF):
    if 'DFF' not in locals():
        DFF = get_feature_template()
    try:
        spk_train = np.array(spk_times)
    
        DFF.spk_num = len(spk_train)
        if len(np.diff(spk_train)) > 0:
            DFF.isi = np.mean(np.diff(spk_train))  # units: seconds
            DFF.isi_std = np.std(np.diff(spk_train))
            DFF.isi_cv = DFF.isi_std / DFF.isi
        
            brst_ar = max_interval(spk_train)
    
            if len(brst_ar) >= 2:
                DFF.brst_num = len(brst_ar)
                DFF.spk_num_brst = sum(map(len, brst_ar)) / len(brst_ar)
                DFF.spk_num_brst_std = np.std(list(map(len, brst_ar)))
                DFF.spk_num_brst_cv = DFF.spk_num_brst_std / DFF.spk_num_brst
        
                DFF.spk_num_non_brst = DFF.spk_num - sum(map(len, brst_ar))
        
                DFF.brst_dur = sum(map(get_brst_dur, brst_ar)) / len(brst_ar)
                DFF.brst_dur_std = np.std(list(map(get_brst_dur, brst_ar)))
                DFF.brst_dur_cv = DFF.brst_dur_std / DFF.brst_dur
        
                DFF.brst_isi = sum(map(get_brst_isi, brst_ar)) / len(brst_ar)
                DFF.brst_isi_std = np.std(list(map(get_brst_isi, brst_ar)))
                DFF.brst_isi_cv = DFF.brst_isi_std / DFF.brst_isi
        
                all_ibi = get_ibi(brst_ar)
                DFF.ibi = np.mean(all_ibi)
                DFF.ibi_std = np.std(all_ibi)
                DFF.ibi_cv = DFF.ibi_std / DFF.ibi
        
                return DFF
            else:
                return DFF
        else:
            return DFF
    except:
        raise
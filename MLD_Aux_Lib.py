# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 16:04:27 2023

@author: meesh
"""

import datetime
import time
import numpy as np

def MLD_ProjectedFinishCalculator(InputToc, CurrentRecord, MaxRecordsCount, StartingRecord=1):
    PassedTime = InputToc.total_seconds()
    if StartingRecord <= 3:
        StartingRecord = 1
    FinishInfoStr = ","
    TotalDuration = (MaxRecordsCount * PassedTime) / (CurrentRecord - StartingRecord + 1)
    FinishInfo = {}
    FinishInfo['Percentage'] = 100 * CurrentRecord / MaxRecordsCount
    FinishInfo['RecordNumber'] = CurrentRecord
    FinishInfo['TimePerRecSec'] = PassedTime / (CurrentRecord - StartingRecord + 1)
    FinishInfo['PassedTimeStr'] = GenerateTotalDurationStr(PassedTime)
    FinishInfo['ProjectedFinishStr'] = (datetime.datetime.now() +
        datetime.timedelta(seconds=(MaxRecordsCount - CurrentRecord) * PassedTime / (CurrentRecord - StartingRecord + 1))).strftime('%m-%d %H:%M:%S')
    FinishInfo['TotalDuration'] = GenerateTotalDurationStr(TotalDuration)
    FinishInfo['RemainingTime'] = GenerateTotalDurationStr((MaxRecordsCount - CurrentRecord) * PassedTime / (CurrentRecord - StartingRecord + 1))
    
    
    FinishMessage = ('\n\tPercentage = {0:.2f}%, Record Number = {1:d}'
                 '\tTime per account = {2:.3f} mSec -- '
                 '\n\tPassed Time = \t\t{3:s},'
                 'Projected Finish = {4:s}'
                 '\n\tRemaining time = \t{5:s}'
                 '\n\tTotal duration = \t{6:s}').format(
                     100*CurrentRecord/MaxRecordsCount,
                     CurrentRecord,
                     1000*PassedTime/(CurrentRecord-StartingRecord+1),
                     GenerateTotalDurationStr(PassedTime),
                     (datetime.datetime.now() + 
                     datetime.timedelta(seconds=(MaxRecordsCount-CurrentRecord)*PassedTime/(CurrentRecord-StartingRecord+1))).strftime('%m-%d %H:%M:%S'),
                     GenerateTotalDurationStr((MaxRecordsCount-CurrentRecord)*PassedTime/(CurrentRecord-StartingRecord+1)),
                     GenerateTotalDurationStr(TotalDuration)
                     )

    return FinishInfo,FinishMessage

def GenerateTotalDurationStr(TotalDur):
    Strings = ['Month', 'Day', 'Hour', 'Minute', 'Second']
    Multipliers = [30, 24, 60, 60, 1]
    Output = ''
    TempDur = TotalDur
    for ctr in range(len(Multipliers)):
        # print(TempDur // (np.prod(Multipliers[ctr:])))
        if ctr < 4:
            TotalTime = (TempDur // (np.prod(Multipliers[ctr:])))
        else:
            TotalTime = (TempDur / (np.prod(Multipliers[ctr:])))
            
        # print(TotalTime)
        if TotalTime > 0:
            if TotalTime == 1:
                TimeSingle = ''
            else:
                TimeSingle = 's'
            
            if ctr < 4 or np.mod(TotalTime,1) == 0:
                Output += f'{TotalTime:.0f} {Strings[ctr]}{TimeSingle}, '
            else:
                Output += f'{TotalTime:.3f} {Strings[ctr]}{TimeSingle}, '
        TempDur -= TotalTime * np.prod(Multipliers[ctr:])
    return Output[:-2]


def MLD_ProjectedFinishCalculator_Sample():
    Start = datetime.datetime.now()
    for qCtr in range(1,int(1e3)):
        time.sleep(int(1.0+np.random.rand(1)*5));
        AA, AAStr = (MLD_ProjectedFinishCalculator(datetime.datetime.now()-Start,qCtr,1e3,1))
        print(AAStr)

MLD_ProjectedFinishCalculator_Sample()
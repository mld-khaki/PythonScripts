# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 16:04:27 2023

@author: meesh
"""

import datetime
import time

def MLD_ProjectedFinishCalculator(InputToc, CurrentRecord, MaxRecordsCount, StartingRecord=1):
    PassedTime = InputToc
    if StartingRecord <= 3:
        StartingRecord = 1
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
    return FinishInfo

def GenerateTotalDurationStr(TotalDur):
    Strings = ['Month', 'Day', 'Hour', 'Minute', 'Second']
    Multipliers = [30, 24, 60, 60, 1]
    Output = ''
    TempDur = TotalDur
    for ctr in range(len(Multipliers)):
        TotalTime = int(TempDur // (prod(Multipliers[ctr:])))
        if TotalTime > 0:
            if TotalTime == 1:
                TimeSingle = ''
            else:
                TimeSingle = 's'
            Output += f'{TotalTime} {Strings[ctr]}{TimeSingle}, '
        TempDur -= TotalTime * prod(Multipliers[ctr:])
    return Output[:-2]


Start = datetime.datetime.now()
for qCtr in range(1,int(1e5)):
    print(MLD_ProjectedFinishCalculator(datetime.datetime.now()-Start,qCtr,1e5,1))
    time.sleep(9);

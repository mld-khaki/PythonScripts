# -*- coding: utf-8 -*-
# mld_aux_lib

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


#%%
import tkinter as tk

class mld_tui:
    def __init__(self):
        self.master = tk.Tk()
        self.master.title("TUI Simulator")

        self.text_widget = tk.Text(self.master, wrap=tk.WORD)
        self.text_widget.pack(expand=True, fill=tk.BOTH)

        self.entry_widget = tk.Entry(self.master)
        self.entry_widget.pack(fill=tk.X)
        self.entry_widget.bind('<Return>', self.process_input)

        self.insert_text("Welcome to the TUI Simulator!\n\n")

    def insert_text(self, text):
        self.text_widget.configure(state=tk.NORMAL)
        self.text_widget.insert(tk.END, text+"\n")
        self.text_widget.see(tk.END)
        self.text_widget.configure(state=tk.DISABLED)
        self.master.update()

    def clear(self):
        self.text_widget.configure(state=tk.NORMAL)
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.see(tk.END)
        self.text_widget.configure(state=tk.DISABLED)
        self.master.update()

    def process_input(self, event):
        user_input = self.entry_widget.get()
        self.entry_widget.delete(0, tk.END)
        self.insert_text(f"> {user_input}\n")

        if user_input.lower() == "exit":
            self.master.quit()
        else:
            self.insert_text(f"Your input was: {user_input}\n")

    def __del__(self):
        if self.master:
            self.master.destroy()    
            
    def on_close(self):
        # if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
        self.master.destroy()

# %timeit MLD_ProjectedFinishCalculator_Sample()
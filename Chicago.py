import pandas as pd
import datetime as dt
from datetime import datetime
import numpy as np
import math
import tkFileDialog

class Chicago:
    def __init__(self):
        self.date = []; self.crime = []
        self.community = []; self.weeks = []
        self.main_crime_type = []
        self.crime_num = []
        self.all_crime_num = []
        self.months = []

    def read_data(self):
        fname = tkFileDialog.askopenfilename(filetypes=(("Template files", "*.csv"), ("All files", "*")))
        data = pd.read_csv(fname, header=0,
                            usecols=["ID", "Date", "Primary Type", "Community Area"],
                            parse_dates=["ID"],
                            names=["ID", "Date", "Primary Type", "Community Area"])
        self.date = data['Date']
        self.crime = list(data['Primary Type'])
        self.community = list(data['Community Area'])

    def get_weeks(self):
        data_num = len(self.date)
        # Compute week number of all date
        self.weeks = [None] * len(self.date)
        month_list = [None]*len(self.date)
        for i in range(data_num):
            if math.isnan(self.community[i]) or self.community[i] == 0:
                self.community[i] = 1
            try:
                d = dt.datetime.strptime(self.date[i], "%m/%d/%Y %H:%M:%S %p")
            except:
                d = dt.datetime.strptime(self.date[i], "%m/%d/%Y %H:%M")
            yy = d.year; mm = d.month
            month_list[i] = str(d.month)+'/'+str(d.year)
            if d.isocalendar()[1] == 1 and d.month == 12:
                self.weeks[i] =(d.year-2013+1)*52
            elif  d.isocalendar()[1] == 52 and d.month==1:
                self.weeks[i] = 1+(d.year-2013)*52
            else:
                self.weeks[i] = d.isocalendar()[1]+(d.year-2013)*52
        str_month_temp=list(set(month_list))
        str_month_temp.sort(key=lambda date: datetime.strptime(date, "%m/%Y"))
        self.months = [None]*len(str_month_temp)
        self.months = str_month_temp

    def get_main_crime_type(self):
        crime_type = list(set(self.crime))
        self.main_crime_type = [None]*(len(crime_type))
        self.main_crime_type = crime_type
        self.main_crime_type.insert(0, 'ALL')
    def get_main_crime_num(self):
        data_num = len(self.date)
        # Get data for training
        self.crime_num = np.zeros((len(self.main_crime_type),len(list(set(self.community))),len(list(set(self.weeks)))))
        self.all_crime_num = np.zeros([len(self.main_crime_type),len(list(set(self.weeks)))])
        for i in range(data_num):
            weeks_idx = self.weeks[i] - 1
            community_idx = self.community[i] - 1
            if self.crime[i] in self.main_crime_type:
                crime_idx = self.main_crime_type.index(self.crime[i])
                self.crime_num[crime_idx, int(community_idx), weeks_idx] += 1
                self.all_crime_num[crime_idx, weeks_idx] += 1
                self.all_crime_num[0, weeks_idx] += 1
            self.crime_num[0, int(community_idx), weeks_idx] += 1

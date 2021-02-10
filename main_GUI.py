from Tkinter import *
import tkMessageBox
from Chicago import Chicago
import numpy as np
import calendar
import datetime as dt
from dateutil.relativedelta import relativedelta
from sklearn import gaussian_process
from sklearn.gaussian_process.kernels import (RBF, Matern,ExpSineSquared)
import ttk
from Draw_community_area import draw_community_area
from Draw_Prediction_Graph import draw_prediction_graph

#pyinstaller --noupx --onefile --add-data="Logo.ico;." --add-data="chicago map.jpg;." main_GUI.py

class GUI:
    def __init__(self, parent):
        self.root = parent
        self.root.wm_iconbitmap('Logo.ico')
        # Set initial parameter values
        self.crime_pred = []
        self.sigma = []
        self.crime_type = []
        self.start_month = []
        self.end_month = []
        self.start_week = 1
        self.end_week = 1
        self.period = 1
        self.covariance = 1
        self.ax_num = []
        self.ax_label = []
        self.total_number_community = 77
        self.data = Chicago()
        self.forecast_fig = []
        self.heatmap_fig = []
        guiframe = Frame(parent, width=580, height=220)
        guiframe.pack(expand=False, anchor=CENTER)
        # Button
        self.read_btn = Button(parent, text='Read DB', command=self.read_DB, width=30)
        self.read_btn.place(x=20, y=20)
        self.predict_btn = Button(parent, text='Show Heatmap', command=self.predict, width=30)
        self.predict_btn.place(x=20, y=80)
        self.display_btn = Button(parent, text='Show Prediction', command=self.show_result, width=30)
        self.display_btn.place(x=20, y=140)
        self.exit = Button(parent,text='Exit', command=self.root.destroy, width=19)
        self.exit.place(x=400, y=180)
        # Checkbox to save heatmap and prediction graph
        self.save_heatmap_var = IntVar()
        self.save_heatmap_var.set(1)
        self.save_heatmap_checkbox = Checkbutton(parent, text='Save Heatmap',variable=self.save_heatmap_var)
        self.save_heatmap_checkbox.place(x=10, y=180)
        self.save_graph_var = IntVar()
        self.save_graph_var.set(1)
        self.save_graph_checkbox = Checkbutton(parent, text='Save Prediction Graph',variable=self.save_graph_var)
        self.save_graph_checkbox.place(x=150, y=180)
        # Labels
        self.Label1 = Label(parent, text='Crime Type:')
        self.Label1.place(x=330,y=20)
        self.Label2 = Label(parent, text='Start Month:')
        self.Label2.place(x=327,y=50)
        self.Label3 = Label(parent, text='End Month:')
        self.Label3.place(x=333,y=80)
        self.Label4 = Label(parent, text='Choose Period to Predict:')
        self.Label4.place(x=260,y=110)
        self.Label5 = Label(parent, text='Covariance Function:')
        self.Label5.place(x=280,y=140)
        ## ComboBox
        # Crime type combobox
        crime_type_str = StringVar()
        self.crime_cbx = ttk.Combobox(parent, textvariable=crime_type_str, state='readonly')
        self.crime_cbx["values"] = 'none'; self.crime_cbx.place(x=400,y=20)
        # Start Month combobox
        start_month_str = StringVar()
        self.start_month_cbx = ttk.Combobox(parent, textvariable=start_month_str, state='readonly')
        self.start_month_cbx["values"] = 'none'
        self.start_month_cbx.place(x=400, y=50)
        # End Month combobox
        end_month_str = StringVar()
        self.end_month_cbx = ttk.Combobox(parent, textvariable=end_month_str, state='readonly')
        self.end_month_cbx["values"] = 'none'; self.end_month_cbx.place(x=400,y=80)
        # Chooose Period to Predict combobox
        period_str = StringVar()
        self.periode_cbx = ttk.Combobox(parent, textvariable=period_str, state='readonly')
        self.periode_cbx["values"] = ['1 Week', '2 Week','3 Week','4 Week']
        self.periode_cbx.place(x=400,y=110)
        # End Month combobox
        covaiance_str = StringVar()
        self.covariance_cbx = ttk.Combobox(parent, textvariable=covaiance_str,state='readonly')
        self.covariance_cbx["values"] = ['Default - Combined', 'Ks','Kt','Kp']; self.covariance_cbx.place(x=400,y=140)

    # Read DB
    def read_DB(self):
        try:
            self.data.read_data()
            self.data.get_weeks()
            self.data.get_main_crime_type()
            self.data.get_main_crime_num()
            self.crime_cbx["values"] = self.data.main_crime_type
            self.crime_cbx.current(0)
            self.start_month_cbx["values"] = self.data.months
            self.start_month_cbx.current(0)
            self.end_month_cbx["values"] = self.data.months
            self.end_month_cbx.current(self.data.months.__len__() - 1)
        except:
            tkMessageBox.showerror("Error", "Please select correct database to read.")

    # Predict crime rate of next weeks and draw heatmap
    def predict(self):
        if self.start_month_cbx.get() == 'none' or self.end_month_cbx.get() == 'none':
            tkMessageBox.showerror("Error", "Please insert the database.")
        else:
            self.get_parameters()
            train_period = self.end_week-self.start_week+1
            if train_period > 1:
                self.crime_pred = np.zeros([self.total_number_community, train_period+self.period])
                self.sigma = np.zeros([self.total_number_community, train_period+self.period])
                for community_num in range(self.total_number_community):
                    # Construct training DB
                    train_DB = np.zeros([train_period, 1])
                    for j in range(train_period):
                        train_DB[j] = float(j+self.start_week)
                    train_Labels = self.data.crime_num[self.data.main_crime_type.index(self.crime_type), community_num, self.start_week-1:self.end_week]
                    for x in range(len(train_Labels)):
                        train_Labels[x] = float(train_Labels[x])

                    # Define Kernel and Gaussian Process
                    l_s = self.total_number_community
                    kernel_s = Matern(length_scale=l_s, length_scale_bounds=(1e-2, 1e5), nu=1.5)
                    l_t = train_period
                    kernel_t = RBF(length_scale=l_t, length_scale_bounds=(1e-2, 1e5))
                    kernel_p = ExpSineSquared(length_scale=l_t, periodicity=52)

                    # Choosing the covariance function
                    if self.covariance == 0:
                        kernel = kernel_t + kernel_s + kernel_t * kernel_s + kernel_p
                    elif self.covariance == 1:
                        kernel = kernel_s
                    elif self.covariance == 2:
                        kernel = kernel_t
                    else:
                        kernel = ExpSineSquared(periodicity=52)

                    gp = gaussian_process.GaussianProcessRegressor(kernel=kernel, alpha=1, n_restarts_optimizer=5)
                    gp.fit(train_DB, train_Labels)
                    # Construct test DB
                    test_DB = np.zeros([train_period+self.period, 1])
                    for j in range(train_period+self.period):
                        test_DB[j] = j+self.start_week
                    self.crime_pred[community_num, :], self.sigma[community_num, :] = gp.predict(test_DB, return_std=True)
                    start_date = dt.datetime.strptime(self.start_month, "%m/%Y")
                    end_date = dt.datetime.strptime(self.end_month, "%m/%Y")
                    img_name = 'Image/Heatmap ' + str(start_date.year) + '.'+str(start_date.month)+'-'\
                               + str(end_date.year) + '.' + str(end_date.month) + \
                               '('+self.crime_type+','+self.periode_cbx.get()+').png'
                draw_community_area(self.crime_pred[:, train_period+self.period-1], self.save_heatmap_var.get(), img_name, self)
            else:
                tkMessageBox.showerror("Error", "Please select dates correctly.")

    # Display prediction results on a graph
    def show_result(self):
        if self.start_month_cbx.get() == 'none' or self.end_month_cbx.get() == 'none':
            tkMessageBox.showerror("Error", "Please insert the database.")
        else:
            self.get_parameters()
            import matplotlib
            matplotlib.rc('xtick', labelsize=8)
            train_period = self.end_week - self.start_week + 1
            # x = str(train_period)
            # end = str(self.end_week)
            # start = str(self.start_week)
            # print x + '=' + end + '-' + start
            if train_period > 1:
                X = np.linspace(self.start_week, self.end_week, self.end_week-self.start_week+1)
                X = np.atleast_2d(X).T
                y = self.data.all_crime_num[self.data.main_crime_type.index(self.crime_type), self.start_week-1:self.end_week]
                # Define Kernel and Gaussian Process
                l_s = self.total_number_community
                kernel_s = Matern(l_s, length_scale_bounds=(1e-2, 1e5),nu=1.5)
                l_t = train_period
                kernel_t = RBF(length_scale=l_t, length_scale_bounds=(1e-2, 1e5))
                kernel_p = ExpSineSquared(length_scale=l_t, periodicity=52)

                # Choosing the covariance function
                if self.covariance == 0:
                    kernel = kernel_t + kernel_s + kernel_t * kernel_s + kernel_p
                elif self.covariance == 1:
                    kernel = kernel_s
                elif self.covariance == 2:
                    kernel = kernel_t
                else:
                    kernel = ExpSineSquared(periodicity=52)

                gp = gaussian_process.GaussianProcessRegressor(kernel=kernel, alpha=0.5, n_restarts_optimizer=10)
                gp.fit(X, y)
                X_pred = np.linspace(self.start_week, self.end_week+self.period, self.end_week-self.start_week+self.period+1)
                X_pred = np.atleast_2d(X_pred).T
                y_pred, sigma_pred = gp.predict(X_pred, return_std=True)
                draw_prediction_graph(self, X, y, X_pred, y_pred, sigma_pred, self.covariance, self.save_graph_var.get())
            else:
                tkMessageBox.showerror("Error", "Please select dates correctly.")

    # Get  parameters Crime types
    def get_parameters(self):
        self.ax_num = []
        self.ax_label = []
        # Get Crime type
        self.crime_type = self.crime_cbx.get()
        # Get Start month
        self.start_month = self.start_month_cbx.get()
        # Get end month
        self.end_month = self.end_month_cbx.get()
        # Start and End points
        start_date = '1/' + self.start_month
        start_t = dt.datetime.strptime(start_date, "%d/%m/%Y") + dt.timedelta(days=1)
        self.start_week = start_t.isocalendar()[1]+(start_t.year-2013)*52
        end_date = dt.datetime.strptime(self.end_month, "%m/%Y")
        end_t = dt.datetime.strptime(str(dt.date(end_date.year, end_date.month, calendar.monthrange(end_date.year,\
                                                        end_date.month)[-1]).day) + '/' + self.end_month, "%d/%m/%Y")
        if end_t.isocalendar()[1] == 1 and end_t.month == 12:
            self.end_week = 52+(end_t.year-2013)*52
        else:
            self.end_week = end_t.isocalendar()[1]+(end_t.year-2013)*52
        self.end_week = min(self.end_week, max(self.data.weeks))

        # Get text of axes
        temp = start_t
        while (temp.year < end_t.year and temp.year != end_t.year) or ((temp.year == end_t.year)
                                                                     and (temp.month <= end_t.month)):
            if temp.isocalendar()[1] >= 52 and temp.month == 1:
                temp_week = 1+(temp.year-2013)*52
            else:
                temp_week = temp.isocalendar()[1] + (temp.year - 2013) * 52
            self.ax_num.append(temp_week)
            self.ax_label.append(str(temp.month)+'/'+str(temp.year))
            temp = temp + relativedelta(months=1)

        # Get period to predict
        self.period = self.periode_cbx["values"].index(self.periode_cbx.get())+1
        # Get covariance kernel
        covariance_str = ['Default - Combined', 'Ks', 'Kt', 'Kp']
        self.covariance = covariance_str.index(self.covariance_cbx.get())


root = Tk()
MainFrame = GUI(root)
MainFrame.crime_cbx.current(0)
MainFrame.start_month_cbx.current(0)
MainFrame.end_month_cbx.current(0)
MainFrame.periode_cbx.current(0)
MainFrame.covariance_cbx.current(0)
root.title('Prediction and Forecasting Crime Rates with Gaussian Processes')
root.attributes('-topmost', 1)
root.resizable(0, 0)
root.protocol('WM_DELETE_WINDOW', root.destroy)
root.mainloop()

from matplotlib import  pyplot as plt
import numpy as np
import datetime as dt


# Draw Prediction graph
def draw_prediction_graph(self, X, y, X_pred, y_pred, sigma_pred, covariance, save_flag):
    dy = max(y)/52*sigma_pred
    confidence_interval = 1.96*dy
    self.forecast_fig = plt.figure(1)
    self.forecast_fig.clf()
    axes = self.forecast_fig.add_subplot(111)
    plt.plot(X, y, 'ro', markersize=3, label=u'Observation')
    plt.plot(X_pred[self.end_week:self.end_week+self.period],
             y_pred[self.end_week:self.end_week+self.period], 'go', markersize=3, label=u'Forecast')
    plt.plot(X_pred, y_pred, 'b-', label=u'Prediction')
    plt.plot([self.end_week, self.end_week], [0, max(y)+100], 'r-')
    plt.fill(np.concatenate([X_pred, X_pred[::-1]]),
             np.concatenate([y_pred - confidence_interval,
                             (y_pred + confidence_interval)[::-1]]),
             alpha=.5, fc='g', ec='None', label='95% confidence interval')
    axes.set_xticks(self.ax_num)
    axes.set_xticklabels(self.ax_label, minor=False, rotation=60)
    axes.set_ylim([-100,max(y)+100])
    if self.crime_type == 'ALL':
        crime_type = self.crime_type + ' crimes'
    else:
        crime_type = self.crime_type
    plt.ylabel('Weekly number of ' + crime_type + ' in Chicago')

    ax = plt.axes()

    period_str = str(self.period)
    covariance_str = ['Combined', 'Ks', 'Kt', 'Kp']
    ax.set_title('Training data: ' + self.start_month + '-' + self.end_month + ',  Crime type: ' + crime_type +\
                 ',  Period to predict: ' + period_str + ' Week,  Covariance: ' + covariance_str[covariance])

    plt.legend(loc='upper left')
    self.forecast_fig.suptitle('Prediction Graph')

    if save_flag == 1:
        start_date = dt.datetime.strptime(self.start_month, "%m/%Y")
        end_date = dt.datetime.strptime(self.end_month, "%m/%Y")
        filename = 'Image/Forecasting ' + str(start_date.year) + '.' + str(start_date.month) + '-' + str(
            end_date.year) + '.' \
                   + str(end_date.month) + '(' + self.crime_type+','+self.periode_cbx.get() + ',' + covariance_str[covariance] + ').png'
        self.forecast_fig.savefig(filename)
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')
    mng.window.title('Prediction Graph')
    mng.window.wm_iconbitmap('Logo.ico')
    mng.window.resizable(0, 0)
    plt.show()



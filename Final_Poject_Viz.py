##This file contains the code for the visualization for the final project.

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider, RangeSlider

# # Fixup data
# data = pd.read_csv("issues.csv")
# data['IssueCreated'] = pd.to_datetime(data['IssueCreated'])
# data['IssueDisp'] = pd.to_datetime(data['IssueDisp'])
# data['Dispositioned By'] = data['Dispositioned By'].fillna(-1).astype(int)
# data['Dispositioned By'] = data['Dispositioned By'].astype(int)
# data = data.dropna(subset=['IssueCreated'])
#
# # Loss by Issue
# issues = pd.DataFrame()
# issues['Issue'] = data['IssueID'].unique()
#
# j = 0
# for i in issues['Issue']:
#     if data[data['IssueID'] == i]['Lot Material Loss'].sum() > 0:
#         temp = data[data['IssueID'] == i]['Lot Material Loss'].sum()
#     else:
#         temp = data[data['IssueID'] == i]['Issue Material Loss'].max()
#     issues.loc[j, 'IssueWeight'] = temp
#     issues.loc[j, 'IssueDate'] = data[data['IssueID'] == i]['IssueCreated'].max()
#     issues.loc[j, 'DispositionedBy'] = data[data['IssueID'] == i]['Dispositioned By'].iloc[0]
#     issues.loc[j, 'Disposition'] = data[data['IssueID'] == i]['Issue Disposition'].iloc[0]
#     issues.loc[j, 'IssueVoid'] = data[data['IssueID'] == i]['Issue Void'].iloc[0]
#     issues.loc[j, 'IssueStatus'] = data[data['IssueID'] == i]['Issue Status'].iloc[0]
#     j += 1

issues = pd.read_csv('issues_short.csv')
issues = issues.dropna()
issues['IssueDate'] = pd.to_datetime(issues['IssueDate'], format='mixed')

# initial year range

init_year_range = [2015, 2020]

# Derived Dataset showing junk material loss by year
loss_by_year = pd.DataFrame()
loss_by_year['Year'] = issues['IssueDate'].dt.year.unique()
j = 0
for i in loss_by_year['Year']:
    loss_by_year.loc[j, 'YearlyLoss'] = issues[issues['IssueDate'].dt.year == i]['IssueWeight'].sum()
    j += 1

# Build Plot
fig, ax = plt.subplots()


def loss_plot(xvals, yvals, curr_ax):
    colors = []
    for x in yvals:
        if x == yvals.max():
            colors.append('red')
        elif x == yvals.min():
            colors.append('green')
        else:
            colors.append('gray')
    curr_ax.clear()
    curr_ax.bar(xvals, yvals, color=colors)
    ax.set_title('Loss by Year')
    ax.set_xlabel('Year')
    ax.set_ylabel('Loss (lbs)')
    ax.set_xlim([xvals.min() - 1, xvals.max() + 1])
    fig.subplots_adjust(bottom=0.25, left=0.25)
    plt.show()


loss_plot(loss_by_year['Year'], loss_by_year['YearlyLoss'], ax)


def dispo_plot(xvals, yvals, curr_ax):
    ops = []
    for x in xvals:

    curr_ax.clear()
    curr_ax.bar(xvals, yvals, color=colors)
    ax.set_title('Loss by Year')
    ax.set_xlabel('Year')
    ax.set_ylabel('Loss (lbs)')
    ax.set_xlim([xvals.min() - 1, xvals.max() + 1])
    fig.subplots_adjust(bottom=0.25, left=0.25)
    plt.show()


axyears = fig.add_axes([0.25, 0.05, 0.5, 0.03])
year_slider = RangeSlider(
    ax=axyears,
    label="Years",
    valmin=loss_by_year['Year'].min(),
    valmax=loss_by_year['Year'].max(),
    valstep=1,
    valinit=(loss_by_year['Year'].min(), loss_by_year['Year'].max())
)


def update_x_limits(val):
    new_min, new_max = val
    new_xvals = loss_by_year[(loss_by_year['Year'] >= new_min) & (loss_by_year['Year'] <= new_max)]['Year']
    new_yvals = loss_by_year[(loss_by_year['Year'] >= new_min) & (loss_by_year['Year'] <= new_max)]['YearlyLoss']
    loss_plot(new_xvals, new_yvals, ax)


year_slider.on_changed(update_x_limits)

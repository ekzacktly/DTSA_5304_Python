############################################################################
# This file contains the code for the visualization for the final project. #
############################################################################

# Import Libraries
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider, RangeSlider

# Import and fix up data
issues = pd.read_csv('issues_short.csv')
issues = issues.dropna()
issues['IssueDate'] = pd.to_datetime(issues['IssueDate'], format='mixed')
issues = issues[issues['DispositionedBy'] != 'Carlos']

# Derived Dataset showing junk material loss by year
loss_by_year = pd.DataFrame()
loss_by_year['Year'] = issues['IssueDate'].dt.year.unique()
j = 0
for i in loss_by_year['Year']:
    loss_by_year.loc[j, 'YearlyLoss'] = issues[issues['IssueDate'].dt.year == i]['IssueWeight'].sum()
    j += 1

# Build figure and plot axes, set background color for contrast
fig, (ax, ax2) = plt.subplots(1, 2, figsize=(12, 6))
fig.subplots_adjust(bottom=0.25, right=0.85, left=0.07, wspace=0.25)
fig.set_facecolor('#F0F0F0')
ax.set_facecolor('#F0F0F0')
ax2.set_facecolor('#F0F0F0')


# First plot function
def loss_plot(xvals, yvals, curr_ax, curr_fig):
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
    curr_ax.set_title('Loss by Year')
    curr_ax.set_xlabel('Year')
    curr_ax.set_ylabel('Loss (lbs)')
    curr_ax.set_xlim([xvals.min() - 1, xvals.max() + 1])
    curr_fig.canvas.draw_idle()


# Call first plot to initialize
loss_plot(loss_by_year['Year'], loss_by_year['YearlyLoss'], ax, fig)


# Second plot function
def dispo_plot(xvals, num_ops, curr_ax, curr_fig):
    curr_ax.clear()
    ops = pd.DataFrame(columns=['Year', 'DispositionedBy', 'Dispositioned'])
    for x in xvals:
        temp = issues[issues['IssueDate'].dt.year == x]['DispositionedBy'].value_counts()
        for i in range(num_ops):
            ops.loc[len(ops)] = [x, temp.index[i], temp[temp.index[i]]]
    op_colors = {}
    colors = [plt.colormaps['flag'](i/len(ops['DispositionedBy'].unique()))
              for i in range(len(ops['DispositionedBy'].unique()))]
    for i, op in enumerate(ops['DispositionedBy'].unique()):
        op_colors[op] = colors[i]
    curr_ax.clear()
    for year in ops['Year'].unique():
        bottom_value = 0
        for dispod_by in ops[ops['Year'] == year]['DispositionedBy']:
            curr_ax.bar(year,
                        ops.loc[(ops['Year'] == year) & (ops['DispositionedBy'] == dispod_by)]['Dispositioned'].item(),
                        bottom=bottom_value, label=dispod_by, color=op_colors[dispod_by])
            bottom_value += (
                ops.loc[(ops['Year'] == year) & (ops['DispositionedBy'] == dispod_by)]['Dispositioned'].item())
    curr_ax.set_title('Dispos by Year')
    curr_ax.set_xlabel('Year')
    curr_ax.set_ylabel('Dispositions')
    curr_ax.set_xlim([xvals.min() - 1, xvals.max() + 1])

    # Deal with Legend
    handles, labels = curr_ax.get_legend_handles_labels()
    unique_handles = []
    unique_labels = []
    for h, l in zip(handles, labels):
        if l not in unique_labels:
            unique_labels.append(l)
            unique_handles.append(h)

    # If there are handles/labels, create/update the legend
    if unique_handles and unique_labels:
        sorted_labels_handles = sorted(zip(unique_labels, unique_handles), key=lambda x: x[0])
        sorted_labels = [label for label, _ in sorted_labels_handles]
        sorted_handles = [handle for _, handle in sorted_labels_handles]
        curr_ax.legend(
            sorted_handles,
            sorted_labels,
            title='Dispo\'d By',
            bbox_to_anchor=(1.02, 0.5),
            loc='center left',
            borderaxespad=0.,
            ncol=max(1, (len(issues['DispositionedBy'].unique()) // 30)),  # Adjust columns based on number of products
            fontsize='x-small'
        )
    # Redraw Canvas
    curr_fig.canvas.draw_idle()


# Call second plot to initialize
dispo_plot(issues['IssueDate'].dt.year.unique(), 5, ax2, fig)

# Build years slider to filter data live
axyears = fig.add_axes([fig.subplotpars.left, 0.1, fig.subplotpars.right-fig.subplotpars.left,0.03])
year_slider = RangeSlider(
    ax=axyears,
    label="Years",
    valmin=loss_by_year['Year'].min(),
    valmax=loss_by_year['Year'].max(),
    valstep=1,
    valinit=(loss_by_year['Year'].min(), loss_by_year['Year'].max())
)

# Update function for years slider
def update_x_limits(val):
    new_min, new_max = val
    new_xvals = loss_by_year[(loss_by_year['Year'] >= new_min) & (loss_by_year['Year'] <= new_max)]['Year']
    new_yvals = loss_by_year[(loss_by_year['Year'] >= new_min) & (loss_by_year['Year'] <= new_max)]['YearlyLoss']
    loss_plot(new_xvals, new_yvals, ax, fig)
    dispo_plot(new_xvals, 5, ax2, fig)


# Call slider update function
year_slider.on_changed(update_x_limits)

# Make plot interactive
plt.show()

import pandas as pd
from scipy.stats import ttest_ind

# Read Excel file and target sheet
excel_path = "Innovation at Uber.xlsx"
data = pd.read_excel(excel_path, sheet_name="Switchbacks")

# Convert 'wait_time' from string to numeric
data['wait_minutes'] = data['wait_time'].str.extract(r'(\d+)').astype(int)

# Select control group entries (2-minute wait, not treated)
control_group = data[data['treat'] == False].copy()

# Total rides = POOL + EXPRESS
control_group['total_rides'] = control_group['trips_pool'] + control_group['trips_express']

# Compute express ride share
control_group['express_ratio'] = control_group['trips_express'] / control_group['total_rides']

# Compute revenue (POOL = $12.5, EXPRESS = $10)
control_group['total_revenue'] = (
        control_group['trips_pool'] * 12.5 + control_group['trips_express'] * 10
)

# Compute profit per ride
control_group['avg_profit'] = (
        control_group['total_revenue'] / control_group['total_rides']
        - control_group['total_driver_payout'] / control_group['total_rides']
)

# Split dataset into commuting vs non-commuting timeframes
peak_time = control_group[control_group['commute'] == True]
off_peak = control_group[control_group['commute'] == False]

# Q1
more_trips_in_peak = peak_time['total_rides'].sum() > off_peak['total_rides'].sum()

# Q2
avg_trip_diff = peak_time['total_rides'].mean() - off_peak['total_rides'].mean()

# Q3
p_val_trip = ttest_ind(peak_time['total_rides'], off_peak['total_rides'], equal_var=False).pvalue
significant_trip = p_val_trip < 0.05

# Q4
higher_express_share = peak_time['express_ratio'].mean() > off_peak['express_ratio'].mean()

# Q5
express_share_diff = peak_time['express_ratio'].mean() - off_peak['express_ratio'].mean()

# Q6
p_val_express = ttest_ind(peak_time['express_ratio'], off_peak['express_ratio'], equal_var=False).pvalue
significant_express = p_val_express < 0.05

# Q7
revenue_gap = peak_time['total_revenue'].mean() - off_peak['total_revenue'].mean()

# Q8
p_val_revenue = ttest_ind(peak_time['total_revenue'], off_peak['total_revenue'], equal_var=False).pvalue
significant_revenue = p_val_revenue < 0.05

# Q9
profit_margin_diff = peak_time['avg_profit'].mean() - off_peak['avg_profit'].mean()

# Q10
p_val_profit = ttest_ind(peak_time['avg_profit'], off_peak['avg_profit'], equal_var=False).pvalue
significant_profit = p_val_profit < 0.05


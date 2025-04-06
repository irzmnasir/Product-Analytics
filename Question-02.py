import pandas as pd
from scipy.stats import ttest_ind

# Read data from Excel
file_name = "Innovation at Uber.xlsx"
uber_data = pd.read_excel(file_name, sheet_name="Switchbacks")

# Extract numeric wait times
uber_data['wait_m'] = uber_data['wait_time'].str.extract(r'(\d+)').astype(int)

# Compute new columns for calculations
uber_data['total_shared_trips'] = uber_data['trips_pool'] + uber_data['trips_express']
uber_data['match_pct'] = uber_data['total_matches'] / uber_data['total_shared_trips']
uber_data['dual_match_pct'] = uber_data['total_double_matches'] / uber_data['total_shared_trips']
uber_data['driver_revenue'] = uber_data['total_driver_payout'] / uber_data['total_shared_trips']

# Divide data by time and treatment
peak = uber_data[uber_data['commute'] == True]
offpeak = uber_data[uber_data['commute'] == False]

treat_peak = peak[peak['treat'] == True]
ctrl_peak = peak[peak['treat'] == False]
treat_offpeak = offpeak[offpeak['treat'] == True]
ctrl_offpeak = offpeak[offpeak['treat'] == False]

# Function for computing difference and significance
def analyze(group_a, group_b):
    delta = group_a.mean() - group_b.mean()
    is_sig = ttest_ind(group_a, group_b, equal_var=False).pvalue < 0.05
    return round(delta, 4), is_sig

# Store analysis
output = {}

# Commuting hour evaluation
output["r1"], _ = analyze(treat_peak['total_shared_trips'], ctrl_peak['total_shared_trips'])
_, output["r2"] = analyze(treat_peak['total_shared_trips'], ctrl_peak['total_shared_trips'])

output["r3"], _ = analyze(treat_peak['rider_cancellations'], ctrl_peak['rider_cancellations'])
_, output["r4"] = analyze(treat_peak['rider_cancellations'], ctrl_peak['rider_cancellations'])

output["r5"], _ = analyze(treat_peak['driver_revenue'], ctrl_peak['driver_revenue'])
_, output["r6"] = analyze(treat_peak['driver_revenue'], ctrl_peak['driver_revenue'])

output["r7"], _ = analyze(treat_peak['match_pct'], ctrl_peak['match_pct'])
_, output["r8"] = analyze(treat_peak['match_pct'], ctrl_peak['match_pct'])

output["r9"], _ = analyze(treat_peak['dual_match_pct'], ctrl_peak['dual_match_pct'])
_, output["r10"] = analyze(treat_peak['dual_match_pct'], ctrl_peak['dual_match_pct'])

# Commute decision logic
sig_all = all([output["r2"], output["r4"], output["r6"], output["r8"], output["r10"]])
valid_trends = (
        output["r1"] > 0 and
        output["r3"] < 0 and
        output["r5"] < 0 and
        output["r7"] > 0 and
        output["r9"] > 0
)

if sig_all and valid_trends:
    output["r11"] = "Yes - clear support"
elif sig_all:
    output["r11"] = "No - clear evidence against"
else:
    output["r11"] = "No - mixed evidence"

# Off-peak evaluation
output["r12"], _ = analyze(treat_offpeak['total_shared_trips'], ctrl_offpeak['total_shared_trips'])
_, output["r13"] = analyze(treat_offpeak['total_shared_trips'], ctrl_offpeak['total_shared_trips'])

output["r14"], _ = analyze(treat_offpeak['rider_cancellations'], ctrl_offpeak['rider_cancellations'])
_, output["r15"] = analyze(treat_offpeak['rider_cancellations'], ctrl_offpeak['rider_cancellations'])

output["r16"], _ = analyze(treat_offpeak['driver_revenue'], ctrl_offpeak['driver_revenue'])
_, output["r17"] = analyze(treat_offpeak['driver_revenue'], ctrl_offpeak['driver_revenue'])

output["r18"], _ = analyze(treat_offpeak['match_pct'], ctrl_offpeak['match_pct'])
_, output["r19"] = analyze(treat_offpeak['match_pct'], ctrl_offpeak['match_pct'])

output["r20"], _ = analyze(treat_offpeak['dual_match_pct'], ctrl_offpeak['dual_match_pct'])
_, output["r21"] = analyze(treat_offpeak['dual_match_pct'], ctrl_offpeak['dual_match_pct'])

# Off-peak decision logic
sig_all_nc = all([output["r13"], output["r15"], output["r17"], output["r19"], output["r21"]])
valid_nc_trends = (
        output["r12"] > 0 and
        output["r14"] < 0 and
        output["r16"] < 0 and
        output["r18"] > 0 and
        output["r20"] > 0
)

if sig_all_nc and valid_nc_trends:
    output["r22"] = "Yes - clear support"
elif sig_all_nc:
    output["r22"] = "No - clear evidence against"
else:
    output["r22"] = "No - mixed evidence"

# Final results
for ref, result in output.items():
    print(f"{ref}: {result}")


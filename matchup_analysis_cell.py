# Matchup Analysis: Which Tactical System Beats Which
# This is the final piece answering the project's core question:
# "which tactical systems perform best against which opposing systems?"

import pandas as pd
import numpy as np

def get_dominant_archetype(team_id, match_id, events_df):
    feat_df = process_match_for_team(team_id, match_id, events_df)
    if feat_df.empty:
        return None
    feat_df['archetype'] = feat_df.apply(lambda row: label_chain_v4(row), axis=1)
    counts = feat_df['archetype'].value_counts()
    counts = counts.drop('Undefined/Other', errors='ignore')
    if counts.empty:
        return None
    return counts.idxmax()

matchup_rows = []

for _, match in matches_ec.iterrows():
    match_id = match['wyId']
    team_ids = match['team_ids']
    if len(team_ids) != 2:
        continue
    team_a_id, team_b_id = int(team_ids[0]), int(team_ids[1])
    team_a_name = team_id_to_name.get(team_a_id, f"Team {team_a_id}")
    team_b_name = team_id_to_name.get(team_b_id, f"Team {team_b_id}")
    style_a = get_dominant_archetype(team_a_id, match_id, events_european_championship_df)
    style_b = get_dominant_archetype(team_b_id, match_id, events_european_championship_df)
    if style_a is None or style_b is None:
        continue
    winner_id = match.get('winner', None)
    if winner_id == team_a_id:
        result_a, result_b = 'W', 'L'
    elif winner_id == team_b_id:
        result_a, result_b = 'L', 'W'
    else:
        result_a = result_b = 'D'
    matchup_rows.append({'match_id': match_id, 'team': team_a_name, 'style': style_a, 'opponent': team_b_name, 'opponent_style': style_b, 'result': result_a})
    matchup_rows.append({'match_id': match_id, 'team': team_b_name, 'style': style_b, 'opponent': team_a_name, 'opponent_style': style_a, 'result': result_b})

matchup_df = pd.DataFrame(matchup_rows)
print(f"Built {len(matchup_df)} team-match rows from {matchup_df['match_id'].nunique()} matches")

win_pct = matchup_df[matchup_df['result'] != 'D'].groupby(['style', 'opponent_style'])['result'].apply(lambda x: (x == 'W').mean() * 100).unstack()
match_count = matchup_df.groupby(['style', 'opponent_style']).size().unstack()

print("WIN RATE (%) - ROW STYLE vs. COLUMN STYLE")
print("(blank = no head-to-head matches in this dataset)")
display(win_pct.round(0))

print("SAMPLE SIZE - number of matches behind each cell above")
display(match_count)

overall = matchup_df.groupby('style')['result'].value_counts().unstack(fill_value=0)
overall['Win %'] = (overall.get('W', 0) / overall.sum(axis=1) * 100).round(1)
print("OVERALL RECORD BY DOMINANT STYLE")
display(overall.sort_values('Win %', ascending=False))

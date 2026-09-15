# Football Tactical Intelligence

Core question: which football tactical systems perform best against which opposing systems?

A personal research project analyzing real match event data to classify teams' possession styles into tactical archetypes, then (as the final step) cross-referencing those archetypes against match outcomes to see which styles tend to beat which.

## Data

Source: Wyscout open football event data (Kaggle), England Premier League and UEFA European Championship event-level data, 1GB+, millions of individual events (passes, shots, duels, etc.) Each row is a single on-ball event with location, time, and outcome, raw material for reconstructing possession sequences.

## Method

Step 1, possession chain extraction. Raw events are grouped into "chains", continuous possession sequences for one team, broken by fouls, throw-ins, goal kicks, or kick-offs.

Step 2, feature engineering. Each chain is scored on: total and max pitch progression, duration, event count, progression speed, directness, backward-pass count, start and end zone, and positional variance.

Step 3, archetype classification. A rule-based classifier (label_chain_v4, iterated through three earlier versions to reduce "Undefined/Other" chains) sorts each chain into one of six tactical archetypes: Fast Transition, Direct Progression, Probing Possession, Circulation, Reset/Recycle, and Short Possession.

Step 4, validation. The classifier was tested on individual matches (Spain, 10 matches) with a chain-by-chain inspector (including simple ASCII pitch visualizations) before scaling up.

Step 5, tournament-wide profiling. Applied across every team and every match in UEFA Euro 2016 (24 teams), producing a per-team tactical profile: how often each team uses each archetype, both as a percentage and as a per-90-minutes rate.

## Results so far

Team possession-chain volume per 90 minutes varied substantially, from Germany and Spain (about 100-108 chains per 90) down to Iceland (about 43 chains per 90), reflecting real differences in tempo and possession style across the tournament, not just classification noise. Full per-team archetype breakdowns (percentage and per-90 rate for all 6 archetypes, all 24 teams) are in the notebook.

## Status: in progress, the final step

Everything above answers "how does each team play?", it doesn't yet answer the project's actual core question: "which style beats which?" The next (and final) step links each match's two teams' dominant archetypes to the actual match result (win, loss, or draw, from Wyscout's match data), producing a style-vs-style win-rate matrix. The code for this step is written (matchup_analysis_cell.py in this repo) but not yet run, it needs to be executed in the original Colab environment against the full dataset.

## Tools

Python (pandas, numpy), Google Colab, Kaggle (Wyscout open data)

## Files

Football_Archtypes_Updated_(2).ipynb is the full analysis notebook (chain extraction, feature engineering, classification, validation, tournament-wide profiling). matchup_analysis_cell.py is the final analysis step (style-vs-style win rates), ready to paste into the notebook and run.

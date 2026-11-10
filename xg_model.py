"""
xG (Expected Goals) Model
=====================================================

OVERVIEW
-----------------------------------------------------
Expected goals (xG) is the probability that a given shot becomes a goal,
estimated from the circumstances of the shot, such as where it was taken,
with which body part, under pressure or not, etc. Summing xG over a player's
or team's shots shows how many goals they 'should' have scored, which can be
a better measure of chance quality than raw shot or goal counts.

This script builds an xG model as a binary classification problem:
    - Input: Features describing a single shot
    - Target: `is_goal` (0 = NO GOAL, 1 = GOAL)
    - Output: Calibrated probability between 0 and 1 for every shot

The goal is not just to separate goals from misses, but to produce well-
calibrated probabilities (shots given 0.20 xG should be scored roughly 20%
of the time).


DATA
-----------------------------------------------------
Source  :   StatsBomb Open Data, accessed through the `statesbombpy package
Scope   :   Competitions are chosen via COMPETITION_ID / DEASON_ID in the CONFIG
            section. Defaults to 2018 FIFA World Cup (43 / 3). Use
            `sb.competitions()` to list other available pairs.
Notes   :   Penalties are excluded due to being shot at a fixed distance
            with no defenders.


PITCH COORDINATES
-----------------------------------------------------
StatsBomb pitches are 120 x 80 units, and the attacking team always shoots
towards x = 120. The goal center is at (120, 40) and the posts are at
(120, 36) and (120, 44), meaning the goal mouth is 8 units wide.

"""
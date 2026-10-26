# Decision memo: making headline tests reliable

*Written as if for Upworthy's editorial and product leads in early 2014.*

## Summary

Our A/B tests are not producing the evidence we act on. For six months in 2013, more than
a fifth of all tests had broken randomization and nobody noticed. Since then, about 93% of
winning picks have been made before the data could tell the options apart. Four process
changes would fix most of this, and none of them needs new tooling.

## What the data shows

1. **Broken randomization went unnoticed for six months.** A simple sample ratio check
   flags 70% of tests run between June 2013 and January 2014, and almost none outside
   that period (about 0.5%). The problem starts and ends within a single week at each end,
   which points to a serving-system issue rather than editorial practice.

2. **Typical tests are too small to detect realistic effects.** Our largest clean two-arm
   test had about 15,000 impressions per arm and could only detect a change in CTR of 21%
   or more. Most headline changes move CTR by much less.

3. **Most "winners" are indistinguishable from the alternative.** Across 3,467 clean tests
   with a recorded winner, 93.0% of decisions fall within noise, and only 6.3% of picks
   were clearly better than the runner-up. When editors did not pick the top arm, the median
   CTR cost was about 7%, too small for these tests to detect.

## Recommendations

1. **Run a sample ratio check before reading any result.** If arm sizes differ more than
   chance allows (p < 0.001), discard the test and investigate the serving system.
   This alone would have caught the 2013 problem within days.

2. **Set a minimum sample size before launch.** At a 2.4% CTR, detecting a 10% lift needs
   about 65,000 impressions per arm. Tests below that should end as "inconclusive",
   not with a winner.

3. **Report CTR with a confidence interval, not just a winner.** An interval that includes
   zero means the test did not decide anything, and editors should know that.

4. **Record every decision and the reason for it.** Most tests have no recorded winner,
   which makes the process impossible to audit or learn from.

## Expected impact

- Broken randomization would be caught in days instead of six months.
- About 9 in 10 current decisions would be labelled inconclusive. Editors could still
  choose a headline on judgment, but openly, rather than on noise presented as data.
- Tests that do reach the minimum size would produce winners we can trust and learn from.

## What this analysis cannot tell us

- The data covers 2013–2015 and only tests with a recorded winner.
- It does not show whether editors used other signals, such as share rates, when choosing.
- Whether larger tests would change editorial outcomes can only be shown by running them.
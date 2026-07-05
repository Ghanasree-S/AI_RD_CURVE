# AI R&D Assignment — Parametric Curve Fitting

## Problem

We're given a set of (x, y) points sampled from a parametric curve for `6 < t < 60`, and the task is to find three unknowns — theta (θ), M, and X — using these equations:

x = t·cos(θ) - e^(M|t|) · sin(0.3t)·sin(θ) + X
y = 42 + t·sin(θ) + e^(M|t|) · sin(0.3t)·cos(θ)

with bounds:
- 0° < θ < 50°
- -0.05 < M < 0.05
- 0 < X < 100

Basically, given a bunch of (x, y) points, the job is to "join the dots" — find the θ, M, X that make the curve fit the data with minimal error.

## Approach

**Why L1 loss?**
The equation has an absolute value term (`e^(M|t|)`), so the loss naturally comes out as an absolute-value based error too. Sum of absolute differences between predicted and actual points = L1 loss. It's the simplest loss that matches the structure of the problem.

**Why Powell's method?**
Powell's algorithm doesn't need smooth/differentiable slopes to work — it just evaluates function values directly and searches from there. Since our loss function involves absolute values (which create sharp corners, not smooth curves), a gradient-based optimizer wouldn't be a great fit. Powell handles that fine since it doesn't rely on derivatives at all.

## Steps I followed

1. Loaded `xy_data.csv` and pulled out the x and y arrays.
2. Generated `t` using `np.linspace(6, 60, n_points)` since the data is uniformly sampled across that range.
3. Wrote the L1 loss function based on the given parametric equations.
4. Set up the bounds for θ, M, X (converting θ to radians).
5. Ran `scipy.optimize.minimize` with the Powell method to get an initial estimate.
6. Ran the script — it gave me values, but they were stuck in a local minimum (X came out around ~54, which didn't look right).
7. Took those values and plugged the equation into Desmos to visualize the curve against the actual data points.
8. Since the Python result wasn't fitting well, I switched to adjusting θ, M, and X manually using Desmos sliders and compared the curve visually against the data.
9. Found that X = 0 fit much better than the ~54 the script gave — once I set X to 0, the wave lined up properly with the dataset.
10. Fine-tuned from there and landed on final values.

## Result

- θ (theta) = 0.53 radians (~30°)
- M = 0.04
- X = 0

### Desmos submission string
```
\left(t*\cos(0.53)-e^{0.04\left|t\right|}\cdot\sin(0.3t)\sin(0.53)+0,42+t*\sin(0.53)+e^{0.04\left|t\right|}\cdot\sin(0.3t)\cos(0.53)\right)
```

## Why this method 

The Powell optimization from the script alone wasn't enough — it converged to a local minimum (X ≈ 54) that looked mathematically "okay" on paper but didn't actually match the data well when I plotted it. Rather than trust the raw script output blindly, I used Desmos to visually check the fit, and manually adjusted the sliders until the curve actually matched the data points. That's how I caught that X should be 0, not ~54 — the automated result was wrong, and eyeballing it against the plot fixed it.

## Limitations

- The script's optimizer got stuck in a local minimum — next time I'd try a global optimizer like `differential_evolution` instead of Powell, so it doesn't rely on the initial guess as much.
- I relied on manual slider adjustment in Desmos to escape the local minimum, which worked but isn't a repeatable/automated fix. Ideally the script itself should get to the right answer without needing manual visual correction.
- Could try running the optimizer with multiple different initial guesses and picking whichever gives the lowest loss, instead of relying on eyeballing it in Desmos.

## Files

- `answer.py` — script that loads the data and runs the Powell optimization
- `xy_data.csv` — given dataset
- Desmos link used for visualization and manual fitting: https://www.desmos.com/calculator/8h8ws9tieh

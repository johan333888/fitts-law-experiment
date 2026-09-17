# Trembling-Finger Springboard: An AI-Assisted Fitts' Law Experiment

**Live demo:** https://johan333888.github.io/fitts-law-experiment/

**Author:** Johan Olsson

---

## Scenario

The user is an **older adult with a mild hand tremor** using a smartphone. Age-related
conditions such as essential tremor, Parkinson's disease, or simply reduced fine-motor
control are common among older users, yet most touchscreen interfaces are designed and
tested by people with steady hands. Selecting the correct app icon on a crowded home
screen &mdash; especially when icons are small &mdash; can be slow and error-prone for
this population.

## Innovation

Instead of a classic reciprocal point-to-point tapping task, this experiment simulates
the tremor itself: the on-screen pointer does not track the mouse 1:1. A smooth,
multi-frequency oscillation (~3&ndash;6 Hz, modeling a real physiological tremor) is
added to the cursor position, and **the jittered position &mdash; not the raw mouse
position &mdash; is what registers the tap**. This means the *effective* target width
shrinks relative to the visual width as icons get smaller, which is exactly the
mechanism by which tremor disproportionately hurts small-target selection in real life.

The task itself is a full **iPhone-style home-screen (springboard) grid**: on each
trial one grey app icon turns green and must be tapped as fast as possible. Icon size
is manipulated in 5 steps (grid sizes 2×2 up to 7×7 icons, always filling the
entire screen, block order randomized), and target distance varies naturally trial to
trial because the green icon appears at a random grid position. This gives a spread of
both **Width (W)** and **Amplitude/Distance (A)** values needed to fit Fitts' Law.

## Application description

- Single-file HTML/JS/canvas app (`index.html`), no external dependencies.
- Phone-mockup UI (status bar, rounded bezel, home indicator) drawn entirely on canvas.
- 5 grid-size blocks × 5 correct taps each = 25 trials, block order shuffled per run.
- Custom trembling cursor (`cursor: none` + canvas-drawn fingertip) replaces the OS
  pointer; hit-testing uses the jittered position.
- Movement Time (MT) measured with `performance.now()` from target onset to correct tap;
  mis-taps are logged as errors but do not stop the timer, so MT reflects real
  “time to successfully acquire the target”.
- On completion, trial data (`trial, block, gridLevel, W_px, A_px, MT_ms, errors,
  timestamp`) is exported as `trials.csv` via a client-side download.

## Why this design? What real-world HCI problem does it address?

Accessible design guidelines (e.g. WCAG target-size recommendations) exist partly
*because* of populations like tremor-affected older adults, but abstract guidelines
("make targets at least 44×44 px") don't show *why* that number matters. By
simulating the tremor directly in the pointer rather than just asking a steady-handed
participant to "imagine" a tremor, this experiment produces real, personally
representative Fitts' Law constants (`a`, `b`) for a tremor-affected pointing
condition, and lets a designer read off directly how much slower/harder small targets
become for this group &mdash; a concrete, data-driven argument for minimum touch-target
sizes in interfaces meant for older or motor-impaired users.

## Your Custom Formula

Fitted by least-squares regression on 25 trials (`python analyze.py data/trials.csv`):

```
MT = a + b · log2(A / W + 1)
MT = 381.9 + 288.0 · log2(A / W + 1)   [ms]
R² = 0.381
Throughput (IP) ≈ 3.47 bits/s
```

## Screen recording

[Watch the experiment recording](results/demo.mov) &mdash; a full run of all 25 trials,
recorded while performing the task as the participant.

## Empirical results

![Fitts' Law scatter plot](results/scatter.png)

With n = 25 (one participant, one session) the fit is moderate (R² = 0.38) &mdash; the
tremor simulation adds trial-to-trial timing noise on top of the usual speed/ID
relationship, and 5 blocks × 5 taps is a small sample for a single regression. The
positive slope (b = 288 ms/bit) still clearly shows the expected Fitts' Law effect:
smaller, farther icons take longer to acquire.

## How to reproduce

1. Open the live demo, click **Start experiment**, and complete all 25 trials while
   screen-recording.
2. Click **Download CSV** and save the file as `data/trials.csv` in this repo.
3. `pip install -r requirements.txt`
4. `python analyze.py data/trials.csv` &mdash; prints the fitted `a`, `b`, R², and
   saves `results/scatter.png`.
5. Add your screen recording, commit and push.

## Files

- `index.html` &mdash; the experiment application (deployed via GitHub Pages)
- `analyze.py` &mdash; regression + scatter-plot script
- `requirements.txt` &mdash; Python dependencies for `analyze.py`
- `data/trials.csv` &mdash; raw exported trial data
- `results/scatter.png` &mdash; generated Fitts' Law plot
- `results/demo.mov` &mdash; screen recording of the experiment

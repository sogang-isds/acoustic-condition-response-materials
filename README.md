# Matched Acoustic-Realization Evaluation Materials

This author-neutral repository supports the 22-group matched counterfactual
evaluation in the accompanying ICASSP submission. It makes the test-specific
data processing inspectable without relying on an unavailable manuscript.

## Listening landing page

The repository root is a short listening tour of the paper's central claim:
under the same acoustic reference and generation seed, does changing the text
still produce a meaningful output change? It includes six interpretable
three-system comparisons, one matched 2x2 example for each reported factor,
and links to the complete evidence. The previous all-reference browser is
preserved as `data_card.html`.

## What is included

- all 44 released 5-second reference waveforms (A/B for 22 groups);
- `metadata/matched_acoustic_realization_release.json`: captions, every A/B
  assignment, selection facts, and SHA-256 hashes;
- `metadata/matched_acoustic_realization_conditions.csv`: 88 crossed
  text/reference condition records; and
- `index.html`: a static GitHub-Pages-ready browser for every reference pair.

## Qualitative listener

The [complete listener](./listener/) contains every reported output: 22 groups,
two fixed generation seeds, all three systems, text-only A/B controls, and all
four text/reference cells. It is supplied for qualitative transparency only; the
paper's conclusions use the group-level quantitative analysis.

The [physical-control listener](./physical_controls/) separately exposes the
speed, pitch, and volume interventions. It uses the first recording from every
source class in the full test (4/4/8 examples) and both seeds. All three systems
are shown for speed and pitch. Volume shows RefCon-T2A and ControlFoley only,
because AC-Foley used a different normalization and seed protocol and is not a
matched comparison. The page lets a reader hear the actual 2×2 manipulation
behind the physical results.

## Construction and leakage safeguards

Each group fixes one held-out VGGSound anchor and one endpoint-generation seed.
Text-guided MMAudio renders endpoints A and B. We then retain the first five
seconds and RMS-match each pair. From 30 frozen candidate groups, we select 22
using predeclared checks: endpoint duration at least 7.9 seconds and CLAP
endpoint distance at least 0.15. Eight candidates fail these checks. Selection
is fixed before any AC-T2A generation.

For the AC-T2A test, a system receives only one caption and one released
reference waveform. It never receives the anchor video, raw anchor audio, or a
target waveform. The four cells per group cross text A/B and reference A/B;
two text-only controls and fixed generation seeds 3/4 complete the protocol.
The three compared systems use identical group IDs, captions, reference files,
cell assignments, seeds, duration, and sampling steps.

## Interpretation limits

These endpoints are *matched acoustic realizations*, not a pure-timbre set:
some A/B captions intentionally differ in source identity. Since MMAudio
constructs the endpoints and is the backbone family adapted by RefCon-T2A, this
release supports the reported condition-allocation comparison only. It cannot
by itself establish perceptual quality, full content/timbre disentanglement, or
an architecture-independent ranking.

## Publication note

The endpoint materials existed before this AC-T2A analysis; their construction
is not claimed as this submission's methodological contribution. This release
exists so readers can inspect the exact evaluation assets and preprocessing.
Only generated endpoint waveforms are redistributed here; no original VGGSound
video or raw anchor audio is included.

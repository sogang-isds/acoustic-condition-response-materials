# Matched Acoustic-Realization Evaluation Materials

This author-neutral repository supports the 22-group matched counterfactual
evaluation in the accompanying ICASSP submission. It makes the test-specific
data processing inspectable without relying on an unavailable manuscript.

## What is included

- all 44 released 5-second reference waveforms (A/B for 22 groups);
- `metadata/matched_acoustic_realization_release.json`: captions, every A/B
  assignment, selection facts, and SHA-256 hashes;
- `metadata/matched_acoustic_realization_conditions.csv`: 88 crossed
  text/reference condition records; and
- `index.html`: a static GitHub-Pages-ready browser for every reference pair.

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
The two compared systems use identical group IDs, captions, reference files,
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
Before making the repository public, the release owner must confirm that public
redistribution of these generated endpoint waveforms is permitted.

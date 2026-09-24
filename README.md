# Who Controls the Sound? Evaluation Materials

This author-neutral repository supports the speed, pitch, and volume
counterfactual evaluations in the accompanying ICASSP submission. It makes the
test-specific data processing and exclusions inspectable.

## Listening landing page

The repository root is a short listening tour of the paper's central claim:
under the same acoustic reference and initial noise, does changing the text
still produce a meaningful output change? It includes six deterministic
three-system comparisons, one matched 2x2 example for each physical factor,
and links to the complete evidence and audits.

## Paper-aligned materials

- `physical_controls/`: speed, pitch, and volume listener with no-reference
  controls, both seeds, and three systems;
- `beta_controls/`: RefCon-T2A reference-guidance operating-point listener;
- `data_card_physical.html`: construction, templates, settings, exclusions,
  audit links, and SHA-256 hashes; and
- `audit/`: machine-readable analyses used by the paper.

## Qualitative listener

The [physical-control listener](./physical_controls/) separately exposes the
source class remaining after the common near-silence exclusion (4/4/8 examples)
and both seeds. All three systems are shown for all factors. AC-Foley volume
uses peak normalization off so the controlled gain intervention is preserved.

## Archive — not used in the paper

The [22-group realization listener](./listener/) and its
[data card](./data_card.html) are retained for link stability. They were
removed from the paper because endpoint validity needs perceptual validation.

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

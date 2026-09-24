#!/usr/bin/env python3
"""Build the paper-aligned physical-control listener for web release v0.19."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
WORKSPACE = REPO.parent.parent
PAPER = REPO.parent / "RefCon_T2A_ICASSP2027_v0_19_0_annotated_three_factor"
MULTI = WORKSPACE / "experiments/t2a_attribute_multiclass_causal32_20260910"
LOUD = WORKSPACE / "experiments/t2a_attribute_loudness_causal16x8_20260910"
BETA = WORKSPACE / "experiments/refcon_beta_full_v017_20260923"

SEEDS = (3, 4)
SELECTED = {
    "speed": ("rate", [0, 32, 65, 97]),
    "pitch": ("pitch", [64, 32, 0, 96]),
    "volume": ("loudness", [96, 80, 0, 16, 64, 32, 112, 50]),
}
CHANGES = {
    "speed": "Reference A: 0.70× time stretch (slow); Reference B: 1.40× time stretch (fast).",
    "pitch": "Reference A: −5 semitones (low); Reference B: +5 semitones (high).",
    "volume": "Reference A: −12 dB signal gain (quiet); Reference B: 0 dB (loud).",
}
SYSTEMS = {
    "refcon_t2a": {"name": "RefCon-T2A", "note": "5 s reference"},
    "controlfoley": {
        "name": "ControlFoley",
        "note": "zero-video diagnostic · 5 s semantic / 2 s timbre",
    },
    "acfoley": {
        "name": "AC-Foley",
        "note": "zero-video diagnostic · 2.02 s reference",
    },
}


def metadata_path(factor: str, axis: str) -> Path:
    root = MULTI if factor != "volume" else LOUD
    return root / f"conditions/{axis}/ref_metadata.json"


def run_root(factor: str, axis: str, system: str) -> Path:
    if factor != "volume":
        folder = {"refcon_t2a": "mix", "controlfoley": "controlfoley", "acfoley": "acfoley"}[system]
        return MULTI / f"{folder}/runs/{axis}"
    if system == "acfoley":
        return LOUD / "acfoley_no_peak_norm_diagnostic/runs/loudness"
    folder = {"refcon_t2a": "mix", "controlfoley": "controlfoley"}[system]
    return LOUD / f"{folder}/runs/loudness"


def checked_copy(src: Path, dst: Path) -> None:
    if not src.is_file():
        raise FileNotFoundError(src)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def build_physical() -> dict:
    manifest = {"version": "v0.19", "seeds": list(SEEDS), "axes": []}
    for factor, (axis, items) in SELECTED.items():
        meta = json.loads(metadata_path(factor, axis).read_text())
        axis_entry = {"id": factor, "change": CHANGES[factor], "samples": []}
        for item in items:
            item_id = f"i{item:03d}"
            a = meta[f"{item_id}_p1_r0"]
            b = meta[f"{item_id}_p2_r0"]
            sample = {
                "id": item_id,
                "source_class": a["source_class"],
                "text": {"A": a["caption"], "B": b["caption"]},
                "references": {},
                "systems": {},
            }
            for ref_index, ref_label in enumerate(("A", "B")):
                src = Path(meta[f"{item_id}_p1_r{ref_index}"]["reference"])
                rel = Path(f"audio/{factor}/{item_id}/reference_{ref_label}.wav")
                checked_copy(src, REPO / "physical_controls" / rel)
                sample["references"][ref_label] = rel.as_posix()

            for system, labels in SYSTEMS.items():
                root = run_root(factor, axis, system)
                system_entry = {**labels, "outputs": {}}
                if factor == "volume" and system == "acfoley":
                    system_entry["note"] += " · peak normalization off"
                for seed in SEEDS:
                    out = {}
                    dest = REPO / f"physical_controls/audio/{factor}/{item_id}/seed_{seed}/{system}"
                    for text_index, text_label in ((1, "A"), (2, "B")):
                        src = root / f"seed{seed}/noref/pred/{item_id}_p{text_index}.wav"
                        rel = Path(f"audio/{factor}/{item_id}/seed_{seed}/{system}/no_reference_text_{text_label}.wav")
                        checked_copy(src, REPO / "physical_controls" / rel)
                        out[f"no_reference_text_{text_label}"] = rel.as_posix()
                        for ref_index, ref_label in enumerate(("A", "B")):
                            src = root / f"seed{seed}/ref/pred/{item_id}_p{text_index}_r{ref_index}.wav"
                            rel = Path(
                                f"audio/{factor}/{item_id}/seed_{seed}/{system}/"
                                f"text_{text_label}_reference_{ref_label}.wav"
                            )
                            checked_copy(src, REPO / "physical_controls" / rel)
                            out[f"text_{text_label}_reference_{ref_label}"] = rel.as_posix()
                    system_entry["outputs"][str(seed)] = out
                sample["systems"][system] = system_entry
            axis_entry["samples"].append(sample)
        manifest["axes"].append(axis_entry)
    return manifest


def build_beta(physical: dict) -> dict:
    beta_sources = {
        "0.5": BETA / "beta_0p5/runs",
        "1": None,
        "2": BETA / "beta_2p0/runs",
    }
    chosen = {"speed": "i000", "pitch": "i000", "volume": "i096"}
    table = {
        "speed": {"unit": "Hz", "0.5": [0.08, 0.25], "1": [0.24, 0.18], "2": [0.50, 0.17]},
        "pitch": {"unit": "semitones", "0.5": [2.58, 1.05], "1": [4.62, 0.78], "2": [5.61, 0.36]},
        "volume": {"unit": "LUFS", "0.5": [0.04, 1.55], "1": [-0.50, 1.34], "2": [-0.02, 1.04]},
    }
    manifest = {"version": "v0.19", "seeds": list(SEEDS), "axes": [], "table": table}
    for axis_entry in physical["axes"]:
        factor = axis_entry["id"]
        source_axis = SELECTED[factor][0]
        sample = next(x for x in axis_entry["samples"] if x["id"] == chosen[factor])
        entry = {
            "id": factor,
            "change": axis_entry["change"],
            "sample": {
                "id": sample["id"],
                "source_class": sample["source_class"],
                "text": sample["text"],
                "references": {
                    key: f"../physical_controls/{value}" for key, value in sample["references"].items()
                },
            },
            "betas": {},
        }
        for beta, source in beta_sources.items():
            outputs = {}
            if beta == "1":
                root = run_root(factor, source_axis, "refcon_t2a")
            else:
                root = source / source_axis
            for seed in SEEDS:
                seed_outputs = {}
                for text_index, text_label in ((1, "A"), (2, "B")):
                    for ref_index, ref_label in enumerate(("A", "B")):
                        src = root / f"seed{seed}/ref/pred/{sample['id']}_p{text_index}_r{ref_index}.wav"
                        beta_dir = beta.replace(".", "p")
                        rel = Path(
                            f"audio/{factor}/{sample['id']}/seed_{seed}/beta_{beta_dir}/"
                            f"text_{text_label}_reference_{ref_label}.wav"
                        )
                        checked_copy(src, REPO / "beta_controls" / rel)
                        seed_outputs[f"text_{text_label}_reference_{ref_label}"] = rel.as_posix()
                outputs[str(seed)] = seed_outputs
            entry["betas"][beta] = outputs
        manifest["axes"].append(entry)
    return manifest


def write_manifest(directory: str, data: dict, variable: str) -> None:
    target = REPO / directory
    target.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    (target / "manifest.json").write_text(text)
    (target / "manifest.js").write_text(f"window.{variable} = {json.dumps(data, ensure_ascii=False)};\n")


def copy_audits() -> None:
    target = REPO / "audit"
    target.mkdir(exist_ok=True)
    names = [
        "attribute_transfer_noref_v0.13.0.json",
        "acfoley_volume_two_seed_v0.17.0.json",
        "near_silent_outputs_v0.17.1.json",
        "silence_exclusion_reaggregation_v0.17.1.json",
        "paired_system_differences_v0.17.1.json",
        "output_integrity_v0.17.0.json",
    ]
    names += [
        f"refcon_beta_{beta}_{factor}_v0.17.0.json"
        for beta in ("0p5", "2p0")
        for factor in ("speed", "pitch", "volume")
    ]
    for name in names:
        checked_copy(PAPER / "audit" / name, target / name)


def write_hashes() -> None:
    files = sorted(
        list((REPO / "physical_controls/audio").rglob("*.wav"))
        + list((REPO / "beta_controls/audio").rglob("*.wav"))
    )
    lines = []
    for path in files:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        lines.append(f"{digest}  {path.relative_to(REPO).as_posix()}")
    (REPO / "audit/public_physical_waveforms_sha256.txt").write_text("\n".join(lines) + "\n")


def main() -> None:
    physical = build_physical()
    beta = build_beta(physical)
    write_manifest("physical_controls", physical, "PHYSICAL_DATA")
    write_manifest("beta_controls", beta, "BETA_DATA")
    copy_audits()
    write_hashes()
    print(
        json.dumps(
            {
                "physical_samples": {x["id"]: len(x["samples"]) for x in physical["axes"]},
                "physical_wav": len(list((REPO / "physical_controls/audio").rglob("*.wav"))),
                "beta_wav": len(list((REPO / "beta_controls/audio").rglob("*.wav"))),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()

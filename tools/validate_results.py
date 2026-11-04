# simulated:illustrative; NO PASSING CLAIM; Q-88 -- Version B result validator (ids and numbers only; no passage text)
"""Validate job/results_B/<person>/<id>.json against job/schema.json without any project dependency.

    python tools/validate_results.py            # prints counts per person, writes job/status_B.json

Uses jsonschema when it is importable; otherwise a structural check of the same contract (one object with a
"features" list of objects carrying feature:str, type:str, evidence:list[str], general:bool). Never prints or
copies any text from the item files.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JOB = ROOT / "job"
PERSONS = ["A", "B", "C"]


def item_ids(person: str) -> list[str]:
    ids = []
    with (JOB / "items_B" / person / "items.jsonl").open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            if "item_id" in rec:
                ids.append(rec["item_id"])
            elif "id" in rec:
                ids.append(rec["id"])
    return ids


def make_validator(schema: dict):
    try:
        import jsonschema  # type: ignore

        v = jsonschema.Draft202012Validator(schema)

        def check(obj) -> str | None:
            errs = list(v.iter_errors(obj))
            return None if not errs else "schema: %s" % errs[0].message[:120]

        return check
    except Exception:  # noqa: BLE001

        def check(obj) -> str | None:
            if not isinstance(obj, dict) or "features" not in obj or not isinstance(obj["features"], list):
                return "structure: no features list"
            for i, f in enumerate(obj["features"]):
                if not isinstance(f, dict):
                    return "structure: feature %d not an object" % i
                if not isinstance(f.get("feature"), str) or not f["feature"].strip():
                    return "structure: feature %d has no feature string" % i
                if not isinstance(f.get("type"), str):
                    return "structure: feature %d has no type" % i
                ev = f.get("evidence")
                if not isinstance(ev, list) or not all(isinstance(e, str) for e in ev):
                    return "structure: feature %d evidence not a list of strings" % i
                if not isinstance(f.get("general"), bool):
                    return "structure: feature %d general not boolean" % i
            return None

        return check


def main() -> int:
    schema = json.loads((JOB / "schema.json").read_text(encoding="utf-8"))
    check = make_validator(schema)
    status = {"label": "simulated:illustrative; NO PASSING CLAIM; Q-88; machine_unreviewed", "persons": {}}
    total_missing = total_invalid = total_valid = 0
    for p in PERSONS:
        ids = item_ids(p)
        rdir = JOB / "results_B" / p
        missing, invalid, valid = [], {}, 0
        for i in ids:
            fp = rdir / ("%s.json" % i)
            if not fp.is_file():
                missing.append(i)
                continue
            try:
                txt = fp.read_text(encoding="utf-8").strip()
                if txt.startswith("```"):
                    invalid[i] = "code_fenced"
                    continue
                obj = json.loads(txt)
            except Exception as e:  # noqa: BLE001
                invalid[i] = "json_parse_failed: %s" % str(e)[:80]
                continue
            err = check(obj)
            if err:
                invalid[i] = err
            else:
                valid += 1
        status["persons"][p] = {"items": len(ids), "valid": valid, "missing": missing, "invalid": invalid}
        total_missing += len(missing)
        total_invalid += len(invalid)
        total_valid += valid
        print("person %s: items %d  valid %d  missing %d  invalid %d" % (p, len(ids), valid, len(missing), len(invalid)))
    status["totals"] = {"valid": total_valid, "missing": total_missing, "invalid": total_invalid}
    (JOB / "status_B.json").write_text(json.dumps(status, indent=1, sort_keys=True), encoding="utf-8")
    print("total: valid %d  missing %d  invalid %d  -> job/status_B.json" % (total_valid, total_missing, total_invalid))
    return 0


if __name__ == "__main__":
    sys.exit(main())

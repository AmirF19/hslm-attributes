simulated:illustrative; NO PASSING CLAIM; Q-88; agent output is machine_unreviewed

# Brief for the session running the Version B inventory in this repository

You are a fresh session working in this repository. Your single task: produce the remaining semantic-feature results of Version B — one fresh agent per item, using the prompt files exactly as they are — until every item has a valid result, committing results to this repository as you go. Read `README.md` first; its rules are binding.

## What exists

- 3,543 items under `job/items_B/<person>/<id>.txt` (persons A, B, C; 1,181 each; ids look like `pop-<lemma>`).
- 687 valid results already under `job/results_B/<person>/<id>.json` (A 288, B 222, C 177). Remaining at the start: 2,856 (A 893, C 1,004, B 959).
- `tools/validate_results.py` — run it first: it prints counts per person and writes `job/status_B.json` with `missing` and `invalid` ids per person. That file is your work list; regenerate it after every batch.

## How to generate

1. Load the `workflow-authoring` skill, then run `workflows/inventory_b.js` with the Workflow tool, `args = {"person": "A", "ids": [ ...bare ids from status_B.json... ]}` — a real JSON object, not a string. The owner has opted in to multi-agent orchestration for this job in so many words: "spin an agent up for each word generation; use the prompts I constructed".
2. Batches of at most 500 ids per workflow, one person at a time, in the order A, C, B. Each agent reads `job/items_B/<person>/<id>.txt` with the Read tool, writes `job/results_B/<person>/<id>.json` with the Write tool, and returns `{id, ok, n_features, n_cited}`. It may not read any other file, search, run commands, or quote passage text beyond the short property phrases the task asks for.
3. After each batch: run the validator; open at least ten of the new result files yourself and check for drift (prose, code fences, missing `evidence`, more than about 25 features, passage quotations longer than a phrase); delete and re-run anything invalid or drifting with a fresh agent (never repair a result by hand); then commit: `git add job/results_B job/status_B.json` and a message such as `Version B: person A, batch 1, 500 results` — no generated-by or co-author lines, nothing else in the message — and push your branch.
4. Cost: about 60,000 tokens per item has been measured (the agent's tool-use overhead dominates the 6 KB prompt), so the whole job is on the order of 170 M tokens. Work in batches so an interruption loses little; if credits or limits run out, stop at a batch boundary, commit, and write what remains into `job/status_B.json`'s companion note `job/STATUS_B.md` (counts only).

## Done means

`python tools/validate_results.py` reports 0 missing and 0 invalid for all three persons (or `job/STATUS_B.md` lists the residue with reasons and the re-run attempts), every result committed and pushed, no passage text anywhere you wrote, no attribution lines in any commit. Then tell the owner the final counts per person. The owner pulls the results and runs collection and canonicalisation on their machine; nothing further is expected from you.

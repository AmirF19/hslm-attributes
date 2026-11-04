# Version B status note (counts only)

simulated:illustrative; NO PASSING CLAIM; Q-88; machine_unreviewed

Session stopped at a batch boundary (cloud credits exhausted). All results below are committed on branch `claude/version-b-inventory-4hz2pj`; the push to GitHub was refused (403, Claude GitHub App not installed on the repository), so the branch exists only in the session's local clone until pushed.

| person | items | valid | missing | invalid |
|---|---|---|---|---|
| A | 1181 | 1181 | 0 | 0 |
| B | 1181 | 222 | 959 | 0 |
| C | 1181 | 1177 | 4 | 0 |
| total | 3543 | 2580 | 963 | 0 |

Batches run this session (all 100% ok, no drift found on inspection): A 500, A 393, C 500, C 500.

Remaining work: person C, 4 ids (see `missing` in `job/status_B.json`); person B, 959 ids in two batches (500 + 459). No re-run attempts were needed; no result failed validation.

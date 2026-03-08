# Contributing to z7scan

## Setup

```bash
git clone https://github.com/z7scan/z7scan.git
cd z7scan
pip install -e .
pytest tests/ -v
```

## Signal Development

Each signal lives in `z7scan/signals.py`. Signals must:
- Accept a `ScanToken` and return a `ScanSignal`
- Produce a score between 0–100
- Set `triggered` based on clear on-chain criteria
- Include raw data in the `raw` dict for transparency

## Weights

Current signal weights must sum to 1.0:
- `liquidity_signal`: 0.35
- `volume_signal`: 0.30
- `momentum_signal`: 0.20
- `activity_signal`: 0.15

## Tests

All PRs require tests. Run the suite before submitting:

```bash
pytest tests/ -v --tb=short
```

## Commits

Use Conventional Commits: `feat:`, `fix:`, `test:`, `docs:`, `chore:`

<div align="center">

![z7scan](https://capsule-render.vercel.app/api?type=waving&color=0,0d1f33,60a5fa&height=200&section=header&text=z7scan&fontSize=60&fontColor=60a5fa&fontAlignY=38&desc=AI%20DEX%20Memecoin%20Scanner%20for%20Solana&descAlignY=58&descColor=94a3b8)

</div>

Most scanners show you the price.

z7scan shows you what the price is built on.

Liquidity depth. Volume authenticity. Wallet momentum. DEX presence. Four signals that read the actual trading structure of a memecoin — not the narrative, not the chart. The underlying market mechanics that determine whether a token has real DEX activity or is a ghost on the order book.

Zone 7 was the internal designation for traffic classification in network security — the zone where packets are identified, scored, and either passed or dropped. z7scan applies that same logic to token traffic on Solana DEX. Every token that enters the scanner gets classified: GHOST, FORMING, ACTIVE, or LIVE.

No feelings. No hype. Just the scan.

`CA: coming soon`

---

## What z7scan Reads

Four signals. One scan score. Four phases.

- **Liquidity** — is there real depth? is LP old enough to be real?
- **Volume** — is the 24h volume organic? are unique wallets growing?
- **Momentum** — is buy pressure outpacing sell pressure right now?
- **Activity** — is concentration low? are multiple DEXes listing this?

---

## Phases

| Phase | Score | z7 Read |
|-------|-------|---------|
| GHOST | 0–25 | *"z7scan: no signal. token is invisible on DEX. avoid."* |
| FORMING | 26–50 | *"z7scan: weak signal. early liquidity forming. monitor."* |
| ACTIVE | 51–75 | *"z7scan: scan positive. real volume and wallets detected."* |
| LIVE | 76–100 | *"z7scan: live. AI confirms active DEX presence. signal strong."* |

---

## Install

```bash
pip install z7scan
```

## Usage

```python
from z7scan import scan, scan_batch, hottest, ScanToken

token = ScanToken(
    token_mint="Z7ScanXyz...pump",
    symbol="Z7SCAN",
    dex_volume_24h=35000.0,
    liquidity_depth_usd=12000.0,
    unique_wallets_24h=120,
    buy_sell_ratio=1.4,
    price_change_1h_pct=8.0,
    lp_age_hours=96.0,
    top10_wallet_pct=0.38,
    dex_listing_count=3,
)

report = scan(token)
print(report.phase)       # LIVE
print(report.scan_score)  # 84.2
print(report.z7_read)     # z7scan: live. AI confirms active DEX presence.
print(report.triggered_count)  # 4
```

### Batch

```python
reports = scan_batch([token1, token2, token3])
best = hottest([token1, token2, token3])
```

---

## Signals

### liquidity_signal (weight: 0.35)

```
depth_score = min(liquidity_depth_usd / 200, 100)
bsr_score   = min(buy_sell_ratio * 60, 100)
age_score   = min(lp_age_hours / 2.4, 100)

score = depth_score * 0.5 + bsr_score * 0.3 + age_score * 0.2
triggered = depth >= $5,000 AND bsr >= 0.8 AND lp_age >= 24h
```

### volume_signal (weight: 0.30)

```
vol_score    = min(dex_volume_24h / 500, 100)
wallet_score = min(unique_wallets_24h / 2, 100)
listing_score = min(dex_listing_count * 25, 100)

score = vol_score * 0.5 + wallet_score * 0.35 + listing_score * 0.15
triggered = volume >= $10,000 AND wallets >= 50 AND listings >= 1
```

### momentum_signal (weight: 0.20)

```
pct_score = clamp(price_change_1h_pct + 50, 0, 100)
bsr_score = min(buy_sell_ratio * 55, 100)

score = pct_score * 0.6 + bsr_score * 0.4
triggered = price_change > 0% AND bsr >= 1.0
```

### activity_signal (weight: 0.15)

```
concentration_score = max(0, 100 - top10_wallet_pct * 100)
wallet_score        = min(unique_wallets_24h / 1.5, 100)
listing_score       = min(dex_listing_count * 30, 100)

score = concentration_score * 0.5 + wallet_score * 0.3 + listing_score * 0.2
triggered = top10 < 75% AND listings >= 2 AND wallets >= 30
```

---

## Stack

- **Python** — core scan engine, 185 tests
- **TypeScript** — React dashboard, live scan feed
- **Docker** — containerized deployment
- **GitHub Actions** — CI on Python 3.11 + 3.12

## Tests

```bash
pytest tests/ -v
# 185 passed
```

## License

MIT

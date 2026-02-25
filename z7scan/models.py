from dataclasses import dataclass, field
from enum import Enum


class ScanPhase(str, Enum):
    GHOST = "GHOST"
    FORMING = "FORMING"
    ACTIVE = "ACTIVE"
    LIVE = "LIVE"


@dataclass
class ScanToken:
    token_mint: str
    symbol: str
    dex_volume_24h: float
    liquidity_depth_usd: float
    unique_wallets_24h: int
    buy_sell_ratio: float
    price_change_1h_pct: float
    lp_age_hours: float
    top10_wallet_pct: float
    dex_listing_count: int


@dataclass
class ScanSignal:
    name: str
    weight: float
    triggered: bool
    score: float
    raw: dict = field(default_factory=dict)


@dataclass
class ScanReport:
    token_mint: str
    symbol: str
    phase: ScanPhase
    scan_score: float
    signals: list[ScanSignal]
    z7_read: str

    @property
    def is_live(self) -> bool:
        return self.phase in (ScanPhase.ACTIVE, ScanPhase.LIVE)

    @property
    def triggered_count(self) -> int:
        return sum(1 for s in self.signals if s.triggered)

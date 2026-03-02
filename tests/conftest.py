import pytest
from z7scan.models import ScanPhase, ScanReport, ScanSignal, ScanToken


def make_token(**kwargs) -> ScanToken:
    defaults = dict(
        token_mint="Z7ScanXyz...pump",
        symbol="Z7SCAN",
        dex_volume_24h=25000.0,
        liquidity_depth_usd=8000.0,
        unique_wallets_24h=80,
        buy_sell_ratio=1.2,
        price_change_1h_pct=5.0,
        lp_age_hours=72.0,
        top10_wallet_pct=0.45,
        dex_listing_count=2,
    )
    defaults.update(kwargs)
    return ScanToken(**defaults)


def make_signal(name="liquidity_signal", weight=0.35, triggered=True, score=80.0, raw=None) -> ScanSignal:
    return ScanSignal(
        name=name,
        weight=weight,
        triggered=triggered,
        score=score,
        raw=raw or {},
    )


def make_report(**kwargs) -> ScanReport:
    signals = kwargs.pop(
        "signals",
        [make_signal(weight=0.35, score=85.0), make_signal(name="s2", weight=0.65, score=70.0)],
    )
    defaults = dict(
        token_mint="Z7ScanXyz...pump",
        symbol="Z7SCAN",
        phase=ScanPhase.LIVE,
        scan_score=85.0,
        signals=signals,
        z7_read="z7scan: live. AI confirms active DEX presence. signal strong.",
    )
    defaults.update(kwargs)
    return ScanReport(**defaults)


@pytest.fixture
def live_token():
    return make_token(
        dex_volume_24h=80000.0,
        liquidity_depth_usd=25000.0,
        unique_wallets_24h=200,
        buy_sell_ratio=1.5,
        price_change_1h_pct=12.0,
        lp_age_hours=168.0,
        top10_wallet_pct=0.30,
        dex_listing_count=3,
    )


@pytest.fixture
def active_token():
    return make_token(
        dex_volume_24h=20000.0,
        liquidity_depth_usd=6000.0,
        unique_wallets_24h=60,
        buy_sell_ratio=1.1,
        price_change_1h_pct=3.0,
        lp_age_hours=48.0,
        top10_wallet_pct=0.55,
        dex_listing_count=2,
    )


@pytest.fixture
def forming_token():
    return make_token(
        dex_volume_24h=5000.0,
        liquidity_depth_usd=2000.0,
        unique_wallets_24h=25,
        buy_sell_ratio=0.9,
        price_change_1h_pct=-2.0,
        lp_age_hours=12.0,
        top10_wallet_pct=0.70,
        dex_listing_count=1,
    )


@pytest.fixture
def ghost_token():
    return make_token(
        dex_volume_24h=200.0,
        liquidity_depth_usd=300.0,
        unique_wallets_24h=5,
        buy_sell_ratio=0.3,
        price_change_1h_pct=-25.0,
        lp_age_hours=1.0,
        top10_wallet_pct=0.95,
        dex_listing_count=0,
    )


@pytest.fixture
def token_collection(live_token, active_token, forming_token, ghost_token):
    return [live_token, active_token, forming_token, ghost_token]

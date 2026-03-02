import pytest
from tests.conftest import make_report, make_signal, make_token
from z7scan.models import ScanPhase, ScanReport, ScanSignal, ScanToken


class TestScanPhase:
    def test_ghost_value(self):
        assert ScanPhase.GHOST == "GHOST"

    def test_forming_value(self):
        assert ScanPhase.FORMING == "FORMING"

    def test_active_value(self):
        assert ScanPhase.ACTIVE == "ACTIVE"

    def test_live_value(self):
        assert ScanPhase.LIVE == "LIVE"

    def test_phase_is_str(self):
        assert isinstance(ScanPhase.LIVE, str)

    def test_all_phases_count(self):
        assert len(ScanPhase) == 4

    def test_phase_comparison(self):
        assert ScanPhase.LIVE != ScanPhase.GHOST

    def test_phase_in_list(self):
        assert ScanPhase.ACTIVE in [ScanPhase.ACTIVE, ScanPhase.LIVE]


class TestScanToken:
    def test_token_creation(self):
        t = make_token()
        assert t.symbol == "Z7SCAN"

    def test_token_mint_stored(self):
        t = make_token(token_mint="AbcXyz")
        assert t.token_mint == "AbcXyz"

    def test_dex_volume_stored(self):
        t = make_token(dex_volume_24h=50000.0)
        assert t.dex_volume_24h == 50000.0

    def test_liquidity_depth_stored(self):
        t = make_token(liquidity_depth_usd=12000.0)
        assert t.liquidity_depth_usd == 12000.0

    def test_unique_wallets_stored(self):
        t = make_token(unique_wallets_24h=150)
        assert t.unique_wallets_24h == 150

    def test_buy_sell_ratio_stored(self):
        t = make_token(buy_sell_ratio=1.8)
        assert t.buy_sell_ratio == 1.8

    def test_price_change_stored(self):
        t = make_token(price_change_1h_pct=-10.0)
        assert t.price_change_1h_pct == -10.0

    def test_lp_age_stored(self):
        t = make_token(lp_age_hours=240.0)
        assert t.lp_age_hours == 240.0

    def test_top10_wallet_stored(self):
        t = make_token(top10_wallet_pct=0.60)
        assert t.top10_wallet_pct == 0.60

    def test_dex_listing_count_stored(self):
        t = make_token(dex_listing_count=4)
        assert t.dex_listing_count == 4

    def test_zero_volume(self):
        t = make_token(dex_volume_24h=0.0)
        assert t.dex_volume_24h == 0.0

    def test_zero_wallets(self):
        t = make_token(unique_wallets_24h=0)
        assert t.unique_wallets_24h == 0

    def test_negative_price_change(self):
        t = make_token(price_change_1h_pct=-50.0)
        assert t.price_change_1h_pct == -50.0

    def test_max_concentration(self):
        t = make_token(top10_wallet_pct=1.0)
        assert t.top10_wallet_pct == 1.0


class TestScanSignal:
    def test_signal_creation(self):
        s = make_signal()
        assert s.name == "liquidity_signal"

    def test_weight_stored(self):
        s = make_signal(weight=0.30)
        assert s.weight == 0.30

    def test_triggered_true(self):
        s = make_signal(triggered=True)
        assert s.triggered is True

    def test_triggered_false(self):
        s = make_signal(triggered=False)
        assert s.triggered is False

    def test_score_stored(self):
        s = make_signal(score=65.0)
        assert s.score == 65.0

    def test_raw_defaults_empty(self):
        s = ScanSignal(name="x", weight=0.35, triggered=True, score=80.0)
        assert s.raw == {}

    def test_raw_stored(self):
        s = make_signal(raw={"depth": 8000})
        assert s.raw["depth"] == 8000


class TestScanReport:
    def test_report_creation(self):
        r = make_report()
        assert r.symbol == "Z7SCAN"

    def test_phase_stored(self):
        r = make_report(phase=ScanPhase.ACTIVE)
        assert r.phase == ScanPhase.ACTIVE

    def test_scan_score_stored(self):
        r = make_report(scan_score=72.5)
        assert r.scan_score == 72.5

    def test_is_live_true_for_live(self):
        r = make_report(phase=ScanPhase.LIVE)
        assert r.is_live is True

    def test_is_live_true_for_active(self):
        r = make_report(phase=ScanPhase.ACTIVE)
        assert r.is_live is True

    def test_is_live_false_for_forming(self):
        r = make_report(phase=ScanPhase.FORMING)
        assert r.is_live is False

    def test_is_live_false_for_ghost(self):
        r = make_report(phase=ScanPhase.GHOST)
        assert r.is_live is False

    def test_triggered_count_all(self):
        signals = [make_signal(triggered=True) for _ in range(4)]
        r = make_report(signals=signals)
        assert r.triggered_count == 4

    def test_triggered_count_none(self):
        signals = [make_signal(triggered=False) for _ in range(4)]
        r = make_report(signals=signals)
        assert r.triggered_count == 0

    def test_triggered_count_partial(self):
        signals = [make_signal(triggered=True), make_signal(triggered=False), make_signal(triggered=True)]
        r = make_report(signals=signals)
        assert r.triggered_count == 2

    def test_z7_read_stored(self):
        r = make_report(z7_read="z7scan: live.")
        assert "live" in r.z7_read

    def test_signals_list_stored(self):
        signals = [make_signal()]
        r = make_report(signals=signals)
        assert len(r.signals) == 1

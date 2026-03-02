import pytest
from tests.conftest import make_token
from z7scan.models import ScanPhase, ScanReport
from z7scan.scanner import Z7Scanner, hottest, scan, scan_batch


class TestScan:
    def test_returns_report(self, live_token):
        r = scan(live_token)
        assert isinstance(r, ScanReport)

    def test_symbol_preserved(self, live_token):
        r = scan(live_token)
        assert r.symbol == live_token.symbol

    def test_token_mint_preserved(self, live_token):
        r = scan(live_token)
        assert r.token_mint == live_token.token_mint

    def test_live_token_phase(self, live_token):
        r = scan(live_token)
        assert r.phase in (ScanPhase.LIVE, ScanPhase.ACTIVE)

    def test_ghost_token_phase(self, ghost_token):
        r = scan(ghost_token)
        assert r.phase in (ScanPhase.GHOST, ScanPhase.FORMING)

    def test_four_signals_returned(self, live_token):
        r = scan(live_token)
        assert len(r.signals) == 4

    def test_signal_names(self, live_token):
        r = scan(live_token)
        names = {s.name for s in r.signals}
        assert "liquidity_signal" in names
        assert "volume_signal" in names
        assert "momentum_signal" in names
        assert "activity_signal" in names

    def test_scan_score_range(self, live_token):
        r = scan(live_token)
        assert 0 <= r.scan_score <= 100

    def test_z7_read_populated(self, live_token):
        r = scan(live_token)
        assert r.z7_read and len(r.z7_read) > 0

    def test_is_live_true_for_live(self, live_token):
        r = scan(live_token)
        assert r.is_live is True

    def test_is_live_false_for_ghost(self, ghost_token):
        r = scan(ghost_token)
        assert r.is_live is False

    def test_triggered_count_range(self, live_token):
        r = scan(live_token)
        assert 0 <= r.triggered_count <= 4

    def test_high_score_live_token(self, live_token):
        r = scan(live_token)
        assert r.scan_score > 50

    def test_low_score_ghost_token(self, ghost_token):
        r = scan(ghost_token)
        assert r.scan_score < 50

    def test_scan_score_matches_phase(self, live_token):
        r = scan(live_token)
        if r.phase == ScanPhase.LIVE:
            assert r.scan_score >= 76
        elif r.phase == ScanPhase.ACTIVE:
            assert 51 <= r.scan_score < 76


class TestScanBatch:
    def test_returns_list(self, token_collection):
        results = scan_batch(token_collection)
        assert isinstance(results, list)

    def test_length_matches(self, token_collection):
        results = scan_batch(token_collection)
        assert len(results) == len(token_collection)

    def test_all_reports(self, token_collection):
        results = scan_batch(token_collection)
        assert all(isinstance(r, ScanReport) for r in results)

    def test_empty_list(self):
        assert scan_batch([]) == []

    def test_single_token(self, live_token):
        results = scan_batch([live_token])
        assert len(results) == 1

    def test_order_preserved(self, token_collection):
        results = scan_batch(token_collection)
        for t, r in zip(token_collection, results):
            assert r.symbol == t.symbol

    def test_independent_scores(self):
        t1 = make_token(dex_volume_24h=100000.0, liquidity_depth_usd=50000.0)
        t2 = make_token(dex_volume_24h=100.0, liquidity_depth_usd=50.0)
        results = scan_batch([t1, t2])
        assert results[0].scan_score > results[1].scan_score


class TestHottest:
    def test_returns_report(self, token_collection):
        r = hottest(token_collection)
        assert isinstance(r, ScanReport)

    def test_returns_highest_score(self, token_collection):
        r = hottest(token_collection)
        all_reports = scan_batch(token_collection)
        max_score = max(rep.scan_score for rep in all_reports)
        assert r.scan_score == max_score

    def test_empty_returns_none(self):
        assert hottest([]) is None

    def test_single_token(self, live_token):
        r = hottest([live_token])
        assert r.symbol == live_token.symbol

    def test_live_wins_over_ghost(self, live_token, ghost_token):
        r = hottest([live_token, ghost_token])
        assert r.symbol == live_token.symbol


class TestZ7Scanner:
    def test_scan_method(self, live_token):
        scanner = Z7Scanner()
        r = scanner.scan(live_token)
        assert isinstance(r, ScanReport)

    def test_scan_batch_method(self, token_collection):
        scanner = Z7Scanner()
        results = scanner.scan_batch(token_collection)
        assert len(results) == len(token_collection)

    def test_hottest_method(self, token_collection):
        scanner = Z7Scanner()
        r = scanner.hottest(token_collection)
        assert isinstance(r, ScanReport)

    def test_hottest_empty(self):
        scanner = Z7Scanner()
        assert scanner.hottest([]) is None

    def test_scanner_instance(self):
        scanner = Z7Scanner()
        assert isinstance(scanner, Z7Scanner)

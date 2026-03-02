import pytest
from tests.conftest import make_signal
from z7scan.models import ScanPhase
from z7scan.scorer import classify_phase, compute_scan_score, get_z7_read, triggered_count


class TestComputeScanScore:
    def test_single_signal(self):
        s = [make_signal(weight=1.0, score=80.0)]
        assert compute_scan_score(s) == 80.0

    def test_two_signals(self):
        s = [make_signal(weight=0.6, score=80.0), make_signal(weight=0.4, score=60.0)]
        assert compute_scan_score(s) == pytest.approx(72.0, abs=0.2)

    def test_all_four_signals(self):
        s = [
            make_signal(weight=0.35, score=90.0),
            make_signal(weight=0.30, score=80.0),
            make_signal(weight=0.20, score=70.0),
            make_signal(weight=0.15, score=60.0),
        ]
        result = compute_scan_score(s)
        expected = 90 * 0.35 + 80 * 0.30 + 70 * 0.20 + 60 * 0.15
        assert result == pytest.approx(expected, abs=0.2)

    def test_zero_scores(self):
        s = [make_signal(weight=0.5, score=0.0), make_signal(weight=0.5, score=0.0)]
        assert compute_scan_score(s) == 0.0

    def test_perfect_scores(self):
        s = [make_signal(weight=0.5, score=100.0), make_signal(weight=0.5, score=100.0)]
        assert compute_scan_score(s) == 100.0

    def test_returns_float(self):
        s = [make_signal()]
        assert isinstance(compute_scan_score(s), float)

    def test_rounded_to_one_decimal(self):
        s = [make_signal(weight=0.35, score=33.333), make_signal(weight=0.65, score=66.666)]
        result = compute_scan_score(s)
        assert result == round(result, 1)


class TestClassifyPhase:
    def test_live_at_76(self):
        assert classify_phase(76.0) == ScanPhase.LIVE

    def test_live_at_100(self):
        assert classify_phase(100.0) == ScanPhase.LIVE

    def test_active_at_51(self):
        assert classify_phase(51.0) == ScanPhase.ACTIVE

    def test_active_at_75(self):
        assert classify_phase(75.9) == ScanPhase.ACTIVE

    def test_forming_at_26(self):
        assert classify_phase(26.0) == ScanPhase.FORMING

    def test_forming_at_50(self):
        assert classify_phase(50.9) == ScanPhase.FORMING

    def test_ghost_at_25(self):
        assert classify_phase(25.9) == ScanPhase.GHOST

    def test_ghost_at_zero(self):
        assert classify_phase(0.0) == ScanPhase.GHOST

    def test_boundary_live(self):
        assert classify_phase(75.9) == ScanPhase.ACTIVE
        assert classify_phase(76.0) == ScanPhase.LIVE

    def test_boundary_active(self):
        assert classify_phase(50.9) == ScanPhase.FORMING
        assert classify_phase(51.0) == ScanPhase.ACTIVE

    def test_boundary_forming(self):
        assert classify_phase(25.9) == ScanPhase.GHOST
        assert classify_phase(26.0) == ScanPhase.FORMING


class TestGetZ7Read:
    def test_ghost_read(self):
        r = get_z7_read(ScanPhase.GHOST)
        assert "invisible" in r

    def test_forming_read(self):
        r = get_z7_read(ScanPhase.FORMING)
        assert "weak" in r or "forming" in r

    def test_active_read(self):
        r = get_z7_read(ScanPhase.ACTIVE)
        assert "positive" in r or "volume" in r

    def test_live_read(self):
        r = get_z7_read(ScanPhase.LIVE)
        assert "live" in r or "strong" in r

    def test_all_reads_contain_z7scan(self):
        for phase in ScanPhase:
            assert "z7scan" in get_z7_read(phase)

    def test_returns_string(self):
        assert isinstance(get_z7_read(ScanPhase.LIVE), str)

    def test_all_phases_have_read(self):
        for phase in ScanPhase:
            r = get_z7_read(phase)
            assert r and len(r) > 0


class TestTriggeredCount:
    def test_all_triggered(self):
        signals = [make_signal(triggered=True) for _ in range(4)]
        assert triggered_count(signals) == 4

    def test_none_triggered(self):
        signals = [make_signal(triggered=False) for _ in range(4)]
        assert triggered_count(signals) == 0

    def test_partial(self):
        signals = [make_signal(triggered=True), make_signal(triggered=False)]
        assert triggered_count(signals) == 1

    def test_empty(self):
        assert triggered_count([]) == 0

    def test_returns_int(self):
        assert isinstance(triggered_count([make_signal()]), int)

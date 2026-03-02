import pytest
from tests.conftest import make_report, make_signal
from z7scan.models import ScanPhase
from z7scan.utils.helpers import filter_by_phase, format_report, live_tokens, scan_table, sort_by_score, top_live


class TestFormatReport:
    def test_contains_symbol(self):
        r = make_report(symbol="RKTX")
        assert "RKTX" in format_report(r)

    def test_contains_phase(self):
        r = make_report(phase=ScanPhase.LIVE)
        assert "LIVE" in format_report(r)

    def test_contains_score(self):
        r = make_report(scan_score=85.0)
        assert "85.0" in format_report(r)

    def test_contains_z7_read(self):
        r = make_report(z7_read="z7scan: live.")
        assert "z7scan" in format_report(r)

    def test_contains_signal_names(self):
        signals = [make_signal(name="liquidity_signal")]
        r = make_report(signals=signals)
        assert "liquidity_signal" in format_report(r)

    def test_triggered_marker_present(self):
        signals = [make_signal(triggered=True)]
        r = make_report(signals=signals)
        assert "+" in format_report(r)

    def test_not_triggered_marker_present(self):
        signals = [make_signal(triggered=False)]
        r = make_report(signals=signals)
        assert "-" in format_report(r)

    def test_returns_string(self):
        assert isinstance(format_report(make_report()), str)

    def test_multiline(self):
        r = make_report()
        assert "\n" in format_report(r)

    def test_ghost_phase(self):
        r = make_report(phase=ScanPhase.GHOST)
        assert "GHOST" in format_report(r)


class TestFilterByPhase:
    def test_filter_live(self):
        reports = [
            make_report(phase=ScanPhase.LIVE),
            make_report(phase=ScanPhase.GHOST),
            make_report(phase=ScanPhase.LIVE),
        ]
        result = filter_by_phase(reports, ScanPhase.LIVE)
        assert len(result) == 2

    def test_filter_ghost(self):
        reports = [make_report(phase=ScanPhase.GHOST), make_report(phase=ScanPhase.LIVE)]
        result = filter_by_phase(reports, ScanPhase.GHOST)
        assert len(result) == 1

    def test_filter_empty(self):
        result = filter_by_phase([], ScanPhase.LIVE)
        assert result == []

    def test_filter_no_match(self):
        reports = [make_report(phase=ScanPhase.GHOST)]
        result = filter_by_phase(reports, ScanPhase.LIVE)
        assert result == []

    def test_filter_all_match(self):
        reports = [make_report(phase=ScanPhase.ACTIVE) for _ in range(3)]
        result = filter_by_phase(reports, ScanPhase.ACTIVE)
        assert len(result) == 3

    def test_filter_forming(self):
        reports = [make_report(phase=ScanPhase.FORMING), make_report(phase=ScanPhase.LIVE)]
        result = filter_by_phase(reports, ScanPhase.FORMING)
        assert all(r.phase == ScanPhase.FORMING for r in result)


class TestLiveTokens:
    def test_returns_live_and_active(self):
        reports = [
            make_report(phase=ScanPhase.LIVE),
            make_report(phase=ScanPhase.ACTIVE),
            make_report(phase=ScanPhase.FORMING),
            make_report(phase=ScanPhase.GHOST),
        ]
        result = live_tokens(reports)
        assert len(result) == 2

    def test_empty(self):
        assert live_tokens([]) == []

    def test_all_ghost(self):
        reports = [make_report(phase=ScanPhase.GHOST) for _ in range(3)]
        assert live_tokens(reports) == []

    def test_all_live(self):
        reports = [make_report(phase=ScanPhase.LIVE) for _ in range(3)]
        assert len(live_tokens(reports)) == 3

    def test_is_live_property_used(self):
        r = make_report(phase=ScanPhase.ACTIVE)
        assert r.is_live is True
        result = live_tokens([r])
        assert len(result) == 1


class TestSortByScore:
    def test_descending_default(self):
        reports = [make_report(scan_score=50.0), make_report(scan_score=90.0), make_report(scan_score=70.0)]
        result = sort_by_score(reports)
        assert result[0].scan_score == 90.0
        assert result[-1].scan_score == 50.0

    def test_ascending(self):
        reports = [make_report(scan_score=50.0), make_report(scan_score=90.0)]
        result = sort_by_score(reports, descending=False)
        assert result[0].scan_score == 50.0

    def test_empty(self):
        assert sort_by_score([]) == []

    def test_single_item(self):
        r = make_report(scan_score=75.0)
        result = sort_by_score([r])
        assert result[0].scan_score == 75.0

    def test_does_not_mutate_original(self):
        reports = [make_report(scan_score=50.0), make_report(scan_score=90.0)]
        original_order = [r.scan_score for r in reports]
        sort_by_score(reports)
        assert [r.scan_score for r in reports] == original_order


class TestScanTable:
    def test_contains_header(self):
        reports = [make_report()]
        t = scan_table(reports)
        assert "SYMBOL" in t
        assert "PHASE" in t
        assert "SCORE" in t

    def test_contains_symbol(self):
        reports = [make_report(symbol="RKTX")]
        assert "RKTX" in scan_table(reports)

    def test_separator_present(self):
        reports = [make_report()]
        assert "---" in scan_table(reports)

    def test_empty_list(self):
        t = scan_table([])
        assert "SYMBOL" in t

    def test_multiple_rows(self):
        reports = [make_report(symbol="AAA"), make_report(symbol="BBB")]
        t = scan_table(reports)
        assert "AAA" in t
        assert "BBB" in t

    def test_returns_string(self):
        assert isinstance(scan_table([make_report()]), str)


class TestTopLive:
    def test_returns_top_n(self):
        reports = [
            make_report(phase=ScanPhase.LIVE, scan_score=90.0),
            make_report(phase=ScanPhase.ACTIVE, scan_score=80.0),
            make_report(phase=ScanPhase.LIVE, scan_score=70.0),
            make_report(phase=ScanPhase.GHOST, scan_score=20.0),
        ]
        result = top_live(reports, n=2)
        assert len(result) == 2

    def test_excludes_non_live(self):
        reports = [
            make_report(phase=ScanPhase.GHOST, scan_score=99.0),
            make_report(phase=ScanPhase.LIVE, scan_score=60.0),
        ]
        result = top_live(reports, n=3)
        assert all(r.is_live for r in result)

    def test_empty(self):
        assert top_live([]) == []

    def test_default_n_is_3(self):
        reports = [make_report(phase=ScanPhase.LIVE, scan_score=float(i)) for i in range(10)]
        result = top_live(reports)
        assert len(result) == 3

    def test_sorted_descending(self):
        reports = [
            make_report(phase=ScanPhase.LIVE, scan_score=60.0),
            make_report(phase=ScanPhase.LIVE, scan_score=90.0),
            make_report(phase=ScanPhase.LIVE, scan_score=75.0),
        ]
        result = top_live(reports, n=3)
        assert result[0].scan_score == 90.0

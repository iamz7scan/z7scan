from ..models import ScanPhase, ScanReport


def format_report(report: ScanReport) -> str:
    lines = [
        f"[{report.phase}] {report.symbol} — score: {report.scan_score}",
        f"  {report.z7_read}",
        f"  signals: {report.triggered_count}/4 triggered",
    ]
    for s in report.signals:
        mark = "+" if s.triggered else "-"
        lines.append(f"    {mark} {s.name}: {s.score:.1f} (w={s.weight})")
    return "\n".join(lines)


def filter_by_phase(reports: list[ScanReport], phase: ScanPhase) -> list[ScanReport]:
    return [r for r in reports if r.phase == phase]


def live_tokens(reports: list[ScanReport]) -> list[ScanReport]:
    return [r for r in reports if r.is_live]


def sort_by_score(reports: list[ScanReport], descending: bool = True) -> list[ScanReport]:
    return sorted(reports, key=lambda r: r.scan_score, reverse=descending)


def scan_table(reports: list[ScanReport]) -> str:
    header = f"{'SYMBOL':<10} {'PHASE':<10} {'SCORE':>6} {'SIGNALS':>8}"
    sep = "-" * len(header)
    rows = [
        f"{r.symbol:<10} {r.phase:<10} {r.scan_score:>6.1f} {r.triggered_count:>5}/4"
        for r in reports
    ]
    return "\n".join([header, sep] + rows)


def top_live(reports: list[ScanReport], n: int = 3) -> list[ScanReport]:
    return sort_by_score(live_tokens(reports))[:n]

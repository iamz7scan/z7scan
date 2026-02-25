from .models import ScanReport, ScanToken
from .scorer import classify_phase, compute_scan_score, get_z7_read
from .signals import activity_signal, liquidity_signal, momentum_signal, volume_signal


def scan(token: ScanToken) -> ScanReport:
    signals = [
        liquidity_signal(token),
        volume_signal(token),
        momentum_signal(token),
        activity_signal(token),
    ]
    score = compute_scan_score(signals)
    phase = classify_phase(score)
    return ScanReport(
        token_mint=token.token_mint,
        symbol=token.symbol,
        phase=phase,
        scan_score=score,
        signals=signals,
        z7_read=get_z7_read(phase),
    )


def scan_batch(tokens: list[ScanToken]) -> list[ScanReport]:
    return [scan(t) for t in tokens]


def hottest(tokens: list[ScanToken]) -> ScanReport | None:
    if not tokens:
        return None
    reports = scan_batch(tokens)
    return max(reports, key=lambda r: r.scan_score)


class Z7Scanner:
    def scan(self, token: ScanToken) -> ScanReport:
        return scan(token)

    def scan_batch(self, tokens: list[ScanToken]) -> list[ScanReport]:
        return scan_batch(tokens)

    def hottest(self, tokens: list[ScanToken]) -> ScanReport | None:
        return hottest(tokens)

from .models import ScanPhase, ScanSignal


def compute_scan_score(signals: list[ScanSignal]) -> float:
    return round(sum(s.score * s.weight for s in signals), 1)


def classify_phase(score: float) -> ScanPhase:
    if score >= 76:
        return ScanPhase.LIVE
    if score >= 51:
        return ScanPhase.ACTIVE
    if score >= 26:
        return ScanPhase.FORMING
    return ScanPhase.GHOST


def get_z7_read(phase: ScanPhase) -> str:
    return {
        ScanPhase.GHOST: "z7scan: no signal. token is invisible on DEX. avoid.",
        ScanPhase.FORMING: "z7scan: weak signal. early liquidity forming. monitor.",
        ScanPhase.ACTIVE: "z7scan: scan positive. real volume and wallets detected.",
        ScanPhase.LIVE: "z7scan: live. AI confirms active DEX presence. signal strong.",
    }[phase]


def triggered_count(signals: list[ScanSignal]) -> int:
    return sum(1 for s in signals if s.triggered)

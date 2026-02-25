from .models import ScanSignal, ScanToken


def liquidity_signal(token: ScanToken) -> ScanSignal:
    depth = token.liquidity_depth_usd
    bsr = token.buy_sell_ratio
    age = token.lp_age_hours

    depth_score = min(depth / 200, 100)
    bsr_score = min(bsr * 60, 100)
    age_score = min(age / 2.4, 100)

    score = round(depth_score * 0.5 + bsr_score * 0.3 + age_score * 0.2, 2)
    triggered = depth >= 5000 and bsr >= 0.8 and age >= 24

    return ScanSignal(
        name="liquidity_signal",
        weight=0.35,
        triggered=triggered,
        score=score,
        raw={"depth_usd": depth, "bsr": bsr, "lp_age_h": age},
    )


def volume_signal(token: ScanToken) -> ScanSignal:
    vol = token.dex_volume_24h
    wallets = token.unique_wallets_24h
    listings = token.dex_listing_count

    vol_score = min(vol / 500, 100)
    wallet_score = min(wallets / 2, 100)
    listing_score = min(listings * 25, 100)

    score = round(vol_score * 0.5 + wallet_score * 0.35 + listing_score * 0.15, 2)
    triggered = vol >= 10000 and wallets >= 50 and listings >= 1

    return ScanSignal(
        name="volume_signal",
        weight=0.30,
        triggered=triggered,
        score=score,
        raw={"volume_24h": vol, "wallets": wallets, "listings": listings},
    )


def momentum_signal(token: ScanToken) -> ScanSignal:
    pct = token.price_change_1h_pct
    bsr = token.buy_sell_ratio

    pct_score = min(max(pct + 50, 0), 100)
    bsr_score = min(bsr * 55, 100)

    score = round(pct_score * 0.6 + bsr_score * 0.4, 2)
    triggered = pct > 0 and bsr >= 1.0

    return ScanSignal(
        name="momentum_signal",
        weight=0.20,
        triggered=triggered,
        score=score,
        raw={"price_change_1h": pct, "bsr": bsr},
    )


def activity_signal(token: ScanToken) -> ScanSignal:
    top10 = token.top10_wallet_pct
    wallets = token.unique_wallets_24h
    listings = token.dex_listing_count

    concentration_score = max(0, 100 - top10 * 100)
    wallet_score = min(wallets / 1.5, 100)
    listing_score = min(listings * 30, 100)

    score = round(concentration_score * 0.5 + wallet_score * 0.3 + listing_score * 0.2, 2)
    triggered = top10 < 0.75 and listings >= 2 and wallets >= 30

    return ScanSignal(
        name="activity_signal",
        weight=0.15,
        triggered=triggered,
        score=score,
        raw={"top10_pct": top10, "wallets": wallets, "listings": listings},
    )

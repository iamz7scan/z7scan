import pytest
from tests.conftest import make_token
from z7scan.signals import activity_signal, liquidity_signal, momentum_signal, volume_signal


class TestLiquiditySignal:
    def test_returns_signal(self, live_token):
        s = liquidity_signal(live_token)
        assert s.name == "liquidity_signal"

    def test_weight(self, live_token):
        s = liquidity_signal(live_token)
        assert s.weight == 0.35

    def test_triggered_live(self, live_token):
        s = liquidity_signal(live_token)
        assert s.triggered is True

    def test_not_triggered_ghost(self, ghost_token):
        s = liquidity_signal(ghost_token)
        assert s.triggered is False

    def test_score_range(self, live_token):
        s = liquidity_signal(live_token)
        assert 0 <= s.score <= 100

    def test_score_low_depth(self):
        t = make_token(liquidity_depth_usd=100.0, buy_sell_ratio=0.5, lp_age_hours=2.0)
        s = liquidity_signal(t)
        assert s.score < 30

    def test_score_high_depth(self):
        t = make_token(liquidity_depth_usd=50000.0, buy_sell_ratio=2.0, lp_age_hours=300.0)
        s = liquidity_signal(t)
        assert s.score > 70

    def test_triggered_requires_depth(self):
        t = make_token(liquidity_depth_usd=100.0, buy_sell_ratio=1.5, lp_age_hours=48.0)
        s = liquidity_signal(t)
        assert s.triggered is False

    def test_triggered_requires_bsr(self):
        t = make_token(liquidity_depth_usd=10000.0, buy_sell_ratio=0.5, lp_age_hours=48.0)
        s = liquidity_signal(t)
        assert s.triggered is False

    def test_triggered_requires_age(self):
        t = make_token(liquidity_depth_usd=10000.0, buy_sell_ratio=1.5, lp_age_hours=5.0)
        s = liquidity_signal(t)
        assert s.triggered is False

    def test_raw_keys(self, live_token):
        s = liquidity_signal(live_token)
        assert "depth_usd" in s.raw
        assert "bsr" in s.raw
        assert "lp_age_h" in s.raw

    def test_score_capped_at_100(self):
        t = make_token(liquidity_depth_usd=999999.0, buy_sell_ratio=10.0, lp_age_hours=9999.0)
        s = liquidity_signal(t)
        assert s.score <= 100

    def test_score_floor_zero(self):
        t = make_token(liquidity_depth_usd=0.0, buy_sell_ratio=0.0, lp_age_hours=0.0)
        s = liquidity_signal(t)
        assert s.score >= 0


class TestVolumeSignal:
    def test_returns_signal(self, live_token):
        s = volume_signal(live_token)
        assert s.name == "volume_signal"

    def test_weight(self, live_token):
        s = volume_signal(live_token)
        assert s.weight == 0.30

    def test_triggered_live(self, live_token):
        s = volume_signal(live_token)
        assert s.triggered is True

    def test_not_triggered_ghost(self, ghost_token):
        s = volume_signal(ghost_token)
        assert s.triggered is False

    def test_score_range(self, live_token):
        s = volume_signal(live_token)
        assert 0 <= s.score <= 100

    def test_score_zero_volume(self):
        t = make_token(dex_volume_24h=0.0, unique_wallets_24h=0, dex_listing_count=0)
        s = volume_signal(t)
        assert s.score == 0

    def test_triggered_requires_volume(self):
        t = make_token(dex_volume_24h=500.0, unique_wallets_24h=100, dex_listing_count=2)
        s = volume_signal(t)
        assert s.triggered is False

    def test_triggered_requires_wallets(self):
        t = make_token(dex_volume_24h=50000.0, unique_wallets_24h=10, dex_listing_count=2)
        s = volume_signal(t)
        assert s.triggered is False

    def test_triggered_requires_listing(self):
        t = make_token(dex_volume_24h=50000.0, unique_wallets_24h=100, dex_listing_count=0)
        s = volume_signal(t)
        assert s.triggered is False

    def test_raw_keys(self, live_token):
        s = volume_signal(live_token)
        assert "volume_24h" in s.raw
        assert "wallets" in s.raw
        assert "listings" in s.raw

    def test_score_capped_at_100(self):
        t = make_token(dex_volume_24h=999999.0, unique_wallets_24h=9999, dex_listing_count=99)
        s = volume_signal(t)
        assert s.score <= 100


class TestMomentumSignal:
    def test_returns_signal(self, live_token):
        s = momentum_signal(live_token)
        assert s.name == "momentum_signal"

    def test_weight(self, live_token):
        s = momentum_signal(live_token)
        assert s.weight == 0.20

    def test_triggered_positive_momentum(self, live_token):
        s = momentum_signal(live_token)
        assert s.triggered is True

    def test_not_triggered_negative_pct(self, ghost_token):
        s = momentum_signal(ghost_token)
        assert s.triggered is False

    def test_score_range(self, live_token):
        s = momentum_signal(live_token)
        assert 0 <= s.score <= 100

    def test_triggered_requires_positive_pct(self):
        t = make_token(price_change_1h_pct=-1.0, buy_sell_ratio=1.5)
        s = momentum_signal(t)
        assert s.triggered is False

    def test_triggered_requires_bsr_above_1(self):
        t = make_token(price_change_1h_pct=5.0, buy_sell_ratio=0.9)
        s = momentum_signal(t)
        assert s.triggered is False

    def test_score_negative_price(self):
        t = make_token(price_change_1h_pct=-50.0, buy_sell_ratio=0.1)
        s = momentum_signal(t)
        assert s.score < 10

    def test_raw_keys(self, live_token):
        s = momentum_signal(live_token)
        assert "price_change_1h" in s.raw
        assert "bsr" in s.raw

    def test_score_capped_at_100(self):
        t = make_token(price_change_1h_pct=999.0, buy_sell_ratio=99.0)
        s = momentum_signal(t)
        assert s.score <= 100


class TestActivitySignal:
    def test_returns_signal(self, live_token):
        s = activity_signal(live_token)
        assert s.name == "activity_signal"

    def test_weight(self, live_token):
        s = activity_signal(live_token)
        assert s.weight == 0.15

    def test_triggered_live(self, live_token):
        s = activity_signal(live_token)
        assert s.triggered is True

    def test_not_triggered_ghost(self, ghost_token):
        s = activity_signal(ghost_token)
        assert s.triggered is False

    def test_score_range(self, live_token):
        s = activity_signal(live_token)
        assert 0 <= s.score <= 100

    def test_triggered_requires_low_concentration(self):
        t = make_token(top10_wallet_pct=0.90, dex_listing_count=3, unique_wallets_24h=100)
        s = activity_signal(t)
        assert s.triggered is False

    def test_triggered_requires_listings(self):
        t = make_token(top10_wallet_pct=0.40, dex_listing_count=1, unique_wallets_24h=100)
        s = activity_signal(t)
        assert s.triggered is False

    def test_triggered_requires_wallets(self):
        t = make_token(top10_wallet_pct=0.40, dex_listing_count=3, unique_wallets_24h=10)
        s = activity_signal(t)
        assert s.triggered is False

    def test_raw_keys(self, live_token):
        s = activity_signal(live_token)
        assert "top10_pct" in s.raw
        assert "wallets" in s.raw
        assert "listings" in s.raw

    def test_concentration_score_zero_at_max(self):
        t = make_token(top10_wallet_pct=1.0, dex_listing_count=0, unique_wallets_24h=0)
        s = activity_signal(t)
        assert s.score == 0.0

    def test_score_capped_at_100(self):
        t = make_token(top10_wallet_pct=0.0, dex_listing_count=99, unique_wallets_24h=9999)
        s = activity_signal(t)
        assert s.score <= 100

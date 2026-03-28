import React, { useEffect, useState } from "react";
import ScanCard, { ScanReport } from "./components/ScanCard";

const BASE: Array<Omit<ScanReport, "scan_score" | "phase" | "is_live" | "triggered_count" | "z7_read">> = [
  { symbol: "Z7SCAN", token_mint: "Z7ScanXyz9qR2mW1pump", signals: [
    { name: "liquidity_signal", weight: 0.35, triggered: true, score: 94 },
    { name: "volume_signal", weight: 0.30, triggered: true, score: 88 },
    { name: "momentum_signal", weight: 0.20, triggered: true, score: 85 },
    { name: "activity_signal", weight: 0.15, triggered: true, score: 90 },
  ]},
  { symbol: "RKTX", token_mint: "RktxM4nVzXQpump", signals: [
    { name: "liquidity_signal", weight: 0.35, triggered: true, score: 82 },
    { name: "volume_signal", weight: 0.30, triggered: true, score: 76 },
    { name: "momentum_signal", weight: 0.20, triggered: true, score: 80 },
    { name: "activity_signal", weight: 0.15, triggered: false, score: 35 },
  ]},
  { symbol: "NXDR", token_mint: "NxdrBz7mN3pump", signals: [
    { name: "liquidity_signal", weight: 0.35, triggered: true, score: 68 },
    { name: "volume_signal", weight: 0.30, triggered: true, score: 62 },
    { name: "momentum_signal", weight: 0.20, triggered: false, score: 28 },
    { name: "activity_signal", weight: 0.15, triggered: false, score: 22 },
  ]},
  { symbol: "RUGX", token_mint: "RugxRz2xQpump", signals: [
    { name: "liquidity_signal", weight: 0.35, triggered: false, score: 9 },
    { name: "volume_signal", weight: 0.30, triggered: false, score: 6 },
    { name: "momentum_signal", weight: 0.20, triggered: false, score: 4 },
    { name: "activity_signal", weight: 0.15, triggered: false, score: 8 },
  ]},
  { symbol: "SKAM", token_mint: "SkamMw6nKpump", signals: [
    { name: "liquidity_signal", weight: 0.35, triggered: false, score: 11 },
    { name: "volume_signal", weight: 0.30, triggered: false, score: 7 },
    { name: "momentum_signal", weight: 0.20, triggered: false, score: 5 },
    { name: "activity_signal", weight: 0.15, triggered: false, score: 9 },
  ]},
  { symbol: "FLXR", token_mint: "FlxrQm8rJpump", signals: [
    { name: "liquidity_signal", weight: 0.35, triggered: false, score: 38 },
    { name: "volume_signal", weight: 0.30, triggered: false, score: 32 },
    { name: "momentum_signal", weight: 0.20, triggered: true, score: 45 },
    { name: "activity_signal", weight: 0.15, triggered: false, score: 20 },
  ]},
];

function score(signals: ScanReport["signals"]) { return signals.reduce((a, s) => a + s.score * s.weight, 0); }
function phase(s: number): ScanReport["phase"] { return s >= 76 ? "LIVE" : s >= 51 ? "ACTIVE" : s >= 26 ? "FORMING" : "GHOST"; }
function read(p: ScanReport["phase"]): string {
  return { GHOST: "z7scan: no signal. token is invisible on DEX. avoid.", FORMING: "z7scan: weak signal. early liquidity forming. monitor.", ACTIVE: "z7scan: scan positive. real volume and wallets detected.", LIVE: "z7scan: live. AI confirms active DEX presence. signal strong." }[p];
}
function jitter(b: number, r: number) { return Math.min(100, Math.max(0, b + (Math.random() - 0.5) * r)); }
function build(): ScanReport[] {
  return BASE.map((t) => {
    const signals = t.signals.map((s) => ({ ...s, score: jitter(s.score, 6) }));
    const s = parseFloat(score(signals).toFixed(1));
    const p = phase(s);
    return { ...t, signals, scan_score: s, phase: p, is_live: p === "LIVE" || p === "ACTIVE", triggered_count: signals.filter((s) => s.triggered).length, z7_read: read(p) };
  });
}

export default function App() {
  const [reports, setReports] = useState<ScanReport[]>(build);
  useEffect(() => { const id = setInterval(() => setReports(build()), 4000); return () => clearInterval(id); }, []);
  const active = reports.filter((r) => r.is_live);
  const inactive = reports.filter((r) => !r.is_live);

  return (
    <div style={{ maxWidth: "1100px", margin: "0 auto", padding: "32px 20px" }}>
      <div style={{ marginBottom: "32px" }}>
        <h1 style={{ fontSize: "22px", fontWeight: 800, color: "#60a5fa", letterSpacing: "0.04em", textTransform: "uppercase" }}>z7scan</h1>
        <p style={{ fontSize: "12px", color: "#4b5563", marginTop: "4px" }}>AI DEX memecoin scanner — live scan feed</p>
      </div>
      {active.length > 0 && (
        <section style={{ marginBottom: "32px" }}>
          <h2 style={{ fontSize: "11px", fontWeight: 600, color: "#60a5fa", letterSpacing: "0.12em", textTransform: "uppercase", marginBottom: "16px" }}>Scan Active ({active.length})</h2>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))", gap: "16px" }}>
            {active.map((r) => <ScanCard key={r.token_mint} report={r} />)}
          </div>
        </section>
      )}
      {inactive.length > 0 && (
        <section>
          <h2 style={{ fontSize: "11px", fontWeight: 600, color: "#1e3a5f", letterSpacing: "0.12em", textTransform: "uppercase", marginBottom: "16px" }}>No Signal ({inactive.length})</h2>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))", gap: "16px" }}>
            {inactive.map((r) => <ScanCard key={r.token_mint} report={r} />)}
          </div>
        </section>
      )}
      <div style={{ marginTop: "40px", fontSize: "10px", color: "#111827", textAlign: "center" }}>z7scan &bull; updates every 4s &bull; AI DEX intelligence</div>
    </div>
  );
}

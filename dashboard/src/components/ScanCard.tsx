import React from "react";

export interface ScanReport {
  symbol: string;
  token_mint: string;
  phase: "GHOST" | "FORMING" | "ACTIVE" | "LIVE";
  scan_score: number;
  is_live: boolean;
  triggered_count: number;
  z7_read: string;
  signals: { name: string; weight: number; triggered: boolean; score: number }[];
}

const PHASE_COLOR: Record<ScanReport["phase"], string> = {
  LIVE: "#60a5fa",
  ACTIVE: "#34d399",
  FORMING: "#fbbf24",
  GHOST: "#4b5563",
};

const BAR_BG = "#0d1f33";

export default function ScanCard({ report }: { report: ScanReport }) {
  const color = PHASE_COLOR[report.phase];
  return (
    <div style={{ background: "#050f1e", border: `1px solid ${color}22`, borderRadius: "8px", padding: "20px", fontFamily: "monospace" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "12px" }}>
        <div>
          <div style={{ fontSize: "16px", fontWeight: 700, color: "#e2e8f0" }}>{report.symbol}</div>
          <div style={{ fontSize: "10px", color: "#4b5563", marginTop: "2px" }}>{report.token_mint}</div>
        </div>
        <div style={{ textAlign: "right" }}>
          <div style={{ fontSize: "11px", fontWeight: 700, color, letterSpacing: "0.1em" }}>{report.phase}</div>
          <div style={{ fontSize: "20px", fontWeight: 800, color, lineHeight: 1.2 }}>{report.scan_score.toFixed(1)}</div>
        </div>
      </div>
      <div style={{ marginBottom: "12px" }}>
        {report.signals.map((s) => (
          <div key={s.name} style={{ marginBottom: "6px" }}>
            <div style={{ display: "flex", justifyContent: "space-between", fontSize: "10px", color: s.triggered ? "#94a3b8" : "#374151", marginBottom: "2px" }}>
              <span>{s.name}</span>
              <span style={{ color: s.triggered ? color : "#374151" }}>{s.score.toFixed(1)}</span>
            </div>
            <div style={{ height: "3px", background: BAR_BG, borderRadius: "2px" }}>
              <div style={{ height: "100%", width: `${s.score}%`, background: s.triggered ? color : "#1f2937", borderRadius: "2px", transition: "width 0.6s ease" }} />
            </div>
          </div>
        ))}
      </div>
      <div style={{ fontSize: "10px", color: "#475569", borderTop: "1px solid #0d1f33", paddingTop: "10px" }}>
        <div style={{ marginBottom: "4px" }}>{report.z7_read}</div>
        <div style={{ color: "#334155" }}>{report.triggered_count}/4 signals triggered</div>
      </div>
    </div>
  );
}

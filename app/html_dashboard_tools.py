from __future__ import annotations

import json
import os
from datetime import datetime
from html import escape
from pathlib import Path
from typing import Any, Dict, List, Optional

OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "outputs"))
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def _stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (str, int, float, bool)):
        return str(value)
    if isinstance(value, (dict, list, tuple)):
        try:
            return json.dumps(value, ensure_ascii=False)
        except Exception:
            return str(value)
    return str(value)


def _escape(value: Any) -> str:
    return escape(_stringify(value))


def _normalize_columns(cols: List[Any]) -> List[str]:
    normalized = []
    for c in cols:
        if isinstance(c, dict):
            if "name" in c:
                normalized.append(str(c["name"]))
            elif "label" in c:
                normalized.append(str(c["label"]))
            elif "key" in c:
                normalized.append(str(c["key"]))
            else:
                normalized.append(_stringify(c))
        else:
            normalized.append(_stringify(c))
    return normalized


def _ts() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _safe_name(prefix: str, ext: str) -> str:
    return f"{prefix}_{_ts()}.{ext}"


def save_html_dashboard(
    dashboard_spec: Dict[str, Any],
    filename_prefix: str = "dashboard",
) -> Dict[str, str]:
    """
    Saves an HTML dashboard to local disk.
    dashboard_spec: structured payload produced by root_agent (KPIs, tables, notes, chart series, etc.)
    Returns: {type: "html", path: "...", note: "..."}
    """
    filename = _safe_name(filename_prefix, "html")
    out_path = OUTPUT_DIR / filename

    title = escape(str(dashboard_spec.get("title", "Retail Dashboard")))
    subtitle = escape(str(dashboard_spec.get("subtitle", "")))

    kpis: List[Dict[str, Any]] = dashboard_spec.get("kpis", []) or []
    tables: List[Dict[str, Any]] = dashboard_spec.get("tables", []) or []
    notes: List[str] = dashboard_spec.get("notes", []) or []
    meta: Dict[str, Any] = dashboard_spec.get("meta", {}) or {}

    # Simple inline “bar chart” using HTML only (no JS libs), to keep workshop stable.
    # chart: {"label_key": "...", "value_key": "...", "rows":[{...},{...}]}
    chart = dashboard_spec.get("chart", None)

    def kpi_cards_html() -> str:
        if not kpis:
            return ""
        cards = []
        for k in kpis[:8]:
            label = escape(str(k.get("label", "")))
            value = escape(str(k.get("value", "")))
            delta = (
                escape(str(k.get("delta", ""))) if k.get("delta") is not None else ""
            )
            hint = escape(str(k.get("hint", ""))) if k.get("hint") is not None else ""
            cards.append(
                f"""
              <div class="card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
                {'<div class="kpi-delta">' + delta + '</div>' if delta else ''}
                {'<div class="kpi-hint">' + hint + '</div>' if hint else ''}
              </div>
            """
            )
        return "<div class='kpi-grid'>" + "\n".join(cards) + "</div>"

    def table_html(cols: List[Any], rows: List[Any], caption: str) -> str:
        if not cols:
            cols = sorted({k for r in rows if isinstance(r, dict) for k in r.keys()})
            if not cols:
                max_len = max(
                    (len(r) for r in rows if isinstance(r, (list, tuple))),
                    default=0,
                )
                cols = (
                    [f"col_{i + 1}" for i in range(max_len)] if max_len else ["value"]
                )
        cols = _normalize_columns(cols)
        normalized_rows: List[Dict[str, Any]] = []
        for r in rows[:20]:
            if isinstance(r, dict):
                row_dict = r
            elif isinstance(r, (list, tuple)):
                row_dict = {
                    cols[i]: r[i] if i < len(r) else "" for i in range(len(cols))
                }
            else:
                row_dict = {cols[0]: r}
            normalized_rows.append(row_dict)
        th = "".join(f"<th>{_escape(c)}</th>" for c in cols)
        body_rows = []
        for r in normalized_rows:
            tds = "".join(f"<td>{_escape(r.get(c, ''))}</td>" for c in cols)
            body_rows.append(f"<tr>{tds}</tr>")
        return f"""
          <div class="panel">
            <div class="panel-title">{_escape(caption)}</div>
            <div class="table-wrap">
              <table>
                <thead><tr>{th}</tr></thead>
                <tbody>{''.join(body_rows)}</tbody>
              </table>
            </div>
          </div>
        """

    def tables_html() -> str:
        if not tables:
            return ""
        parts = []
        for t in tables[:4]:
            caption = str(t.get("caption", "Table"))
            cols = t.get("columns", []) or []
            rows = t.get("rows", []) or []
            if isinstance(rows, dict):
                # allow {"rows": [...]} accidental nesting
                rows = rows.get("rows", [])
            parts.append(table_html(cols, rows, caption))
        return "\n".join(parts)

    def notes_html() -> str:
        if not notes:
            return ""
        lis = "".join(f"<li>{escape(str(n))}</li>" for n in notes[:10])
        return f"""
          <div class="panel">
            <div class="panel-title">Notes</div>
            <ul class="notes">{lis}</ul>
          </div>
        """

    def chart_html() -> str:
        if not chart:
            return ""
        rows = chart.get("rows", []) or []
        label_key = chart.get("label_key")
        value_key = chart.get("value_key")

        if not rows or not label_key or not value_key:
            return ""

        # determine max for scaling
        vals = []
        for r in rows[:12]:
            try:
                vals.append(float(r.get(value_key, 0)))
            except Exception:
                vals.append(0.0)
        max_v = max(vals) if vals else 1.0
        if max_v == 0:
            max_v = 1.0

        bars = []
        for r in rows[:12]:
            label = escape(str(r.get(label_key, "")))
            try:
                v = float(r.get(value_key, 0))
            except Exception:
                v = 0.0
            w = int((v / max_v) * 100)
            bars.append(
                f"""
              <div class="bar-row">
                <div class="bar-label">{label}</div>
                <div class="bar-track"><div class="bar-fill" style="width:{w}%"></div></div>
                <div class="bar-value">{escape(str(r.get(value_key,'')))}</div>
              </div>
            """
            )

        return f"""
          <div class="panel">
            <div class="panel-title">{escape(str(chart.get("title","Chart")))}</div>
            <div class="bars">{''.join(bars)}</div>
          </div>
        """

    meta_json = escape(json.dumps(meta, ensure_ascii=False, indent=2)) if meta else ""

    html = f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <style>
    body {{ font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial; margin: 0; background: #f6f7fb; color: #111; }}
    .header {{ padding: 18px 20px; background: white; border-bottom: 1px solid #e7e8ef; }}
    .title {{ font-size: 18px; font-weight: 700; margin: 0; }}
    .subtitle {{ font-size: 13px; color: #555; margin-top: 6px; }}
    .container {{ padding: 16px; max-width: 1100px; margin: 0 auto; }}
    .kpi-grid {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; margin-bottom: 12px; }}
    .card {{ background: white; border: 1px solid #e7e8ef; border-radius: 12px; padding: 12px; box-shadow: 0 1px 2px rgba(0,0,0,0.04); }}
    .kpi-label {{ font-size: 12px; color: #666; }}
    .kpi-value {{ font-size: 22px; font-weight: 800; margin-top: 6px; }}
    .kpi-delta {{ font-size: 12px; margin-top: 4px; }}
    .kpi-hint {{ font-size: 12px; color: #666; margin-top: 6px; }}
    .panel {{ background: white; border: 1px solid #e7e8ef; border-radius: 12px; padding: 12px; margin-top: 12px; }}
    .panel-title {{ font-size: 14px; font-weight: 700; margin-bottom: 10px; }}
    .table-wrap {{ overflow-x: auto; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border-bottom: 1px solid #eee; text-align: left; padding: 8px; font-size: 12px; }}
    th {{ background: #fafafa; font-weight: 700; }}
    .notes {{ margin: 0; padding-left: 18px; }}
    .bar-row {{ display: grid; grid-template-columns: 160px 1fr 80px; gap: 10px; align-items: center; margin: 6px 0; }}
    .bar-label {{ font-size: 12px; color: #444; }}
    .bar-track {{ height: 10px; background: #f0f1f6; border-radius: 999px; overflow: hidden; }}
    .bar-fill {{ height: 10px; background: #4c6fff; border-radius: 999px; }}
    .bar-value {{ font-size: 12px; text-align: right; color: #444; }}
    .meta {{ white-space: pre-wrap; font-size: 11px; background: #fafafa; padding: 10px; border-radius: 8px; border: 1px dashed #ddd; }}
    @media (max-width: 900px) {{
      .kpi-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      .bar-row {{ grid-template-columns: 120px 1fr 70px; }}
    }}
  </style>
</head>
<body>
  <div class="header">
    <div class="title">{title}</div>
    {f'<div class="subtitle">{subtitle}</div>' if subtitle else ''}
  </div>

  <div class="container">
    {kpi_cards_html()}
    {chart_html()}
    {tables_html()}
    {notes_html()}
    {f'<div class="panel"><div class="panel-title">Meta</div><div class="meta">{meta_json}</div></div>' if meta_json else ''}
  </div>
</body>
</html>
"""
    out_path.write_text(html, encoding="utf-8")

    return {
        "type": "html",
        "path": out_path.as_posix(),
        "note": f"Saved dashboard to {out_path.as_posix()}",
    }

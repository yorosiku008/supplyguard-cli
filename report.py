from datetime import datetime
from pathlib import Path
from typing import Dict, List

from rich.console import Console
from rich.table import Table
from rich import box

AXIS_LABELS = {
    'sbom':             ('SBOM/CVE',     '45%'),
    'questionnaire':    ('アンケート',   '35%'),
    'incident_history': ('インシデント', '20%'),
}

GRADE_COLORS = {'S': 'bright_cyan', 'A': 'green', 'B': 'yellow', 'C': 'orange3', 'D': 'red', 'E': 'bright_red'}


def _grade_color(grade: str) -> str:
    return GRADE_COLORS.get(grade, 'white')


def print_report(vendor_scores: List[Dict], ai_suggestions: List[str] = None) -> None:
    console = Console(legacy_windows=False)
    console.print('\n[bold]*** SupplyGuard JP -- サプライチェーン セキュリティ評価[/bold]')
    console.print('=' * 60)
    console.print(f'スキャン日時: {datetime.now().strftime("%Y-%m-%d %H:%M")}')
    console.print(f'評価ベンダー数: {len(vendor_scores)}社')
    console.print()

    table = Table(box=box.SIMPLE, show_header=True, header_style='bold dim')
    table.add_column('ベンダー名', style='white', width=22)
    table.add_column('グレード', width=7)
    table.add_column('スコア', width=7)
    table.add_column('SBOM/CVE', width=10)
    table.add_column('アンケート', width=11)
    table.add_column('インシデント', width=12)
    table.add_column('主な問題', style='dim')

    for vs in vendor_scores:
        grade = vs['grade']
        total = vs['total']
        color = _grade_color(grade)
        axes = vs.get('axes', {})

        sbom_s = axes.get('sbom', {}).get('score', '-')
        q_s = axes.get('questionnaire', {}).get('score', '-')
        inc_s = axes.get('incident_history', {}).get('score', '-')

        all_issues = []
        for ax in AXIS_LABELS:
            all_issues.extend(axes.get(ax, {}).get('issues', []))
        issue_text = all_issues[0] if all_issues else '問題なし'

        table.add_row(
            vs.get('vendor', '不明'),
            f'[{color}]{grade}[/{color}]',
            f'[{color}]{total}[/{color}]',
            str(sbom_s),
            str(q_s),
            str(inc_s),
            issue_text,
        )

    console.print(table)

    for vs in vendor_scores:
        axes = vs.get('axes', {})
        all_issues = []
        for ax in AXIS_LABELS:
            all_issues.extend(axes.get(ax, {}).get('issues', []))
        if all_issues:
            console.print(f'[bold]{vs.get("vendor", "不明")} -- 改善が必要な項目:[/bold]')
            for i, issue in enumerate(all_issues, 1):
                console.print(f'  {i}. {issue}')
    console.print()

    if ai_suggestions:
        console.print('[bold bright_cyan]Claude AI 対応提案:[/bold bright_cyan]')
        for suggestion in ai_suggestions:
            console.print(f'  {suggestion}')
        console.print()


def build_md_report(vendor_scores: List[Dict], ai_suggestions: List[str] = None) -> str:
    lines = [
        '# SupplyGuard JP -- サプライチェーン セキュリティ評価レポート',
        '',
        f'**スキャン日時:** {datetime.now().strftime("%Y-%m-%d %H:%M")}',
        f'**評価ベンダー数:** {len(vendor_scores)}社',
        '',
        '## ベンダー別スコア',
        '',
        '| ベンダー名 | グレード | 総合スコア | SBOM/CVE | アンケート | インシデント |',
        '|---|---|---|---|---|---|',
    ]

    for vs in vendor_scores:
        axes = vs.get('axes', {})
        lines.append(
            f'| {vs.get("vendor", "不明")} | {vs["grade"]} | {vs["total"]} '
            f'| {axes.get("sbom", {}).get("score", "-")} '
            f'| {axes.get("questionnaire", {}).get("score", "-")} '
            f'| {axes.get("incident_history", {}).get("score", "-")} |'
        )

    lines += ['', '## 改善項目', '']
    for vs in vendor_scores:
        axes = vs.get('axes', {})
        for ax, (label, _) in AXIS_LABELS.items():
            for issue in axes.get(ax, {}).get('issues', []):
                lines.append(f'- [{vs.get("vendor", "不明")} / {label}] {issue}')

    if ai_suggestions:
        lines += ['', '## Claude AI 対応提案', '']
        for suggestion in ai_suggestions:
            lines.append(f'- {suggestion}')

    return '\n'.join(lines)


def save_md_report(content: str, path: str) -> None:
    Path(path).write_text(content, encoding='utf-8')

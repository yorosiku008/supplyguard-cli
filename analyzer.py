from typing import Dict, List
import anthropic

VENDOR_ANALYSIS_PROMPT = """あなたはサプライチェーンセキュリティの専門家です。
以下のベンダーリスク評価データを分析し、調達担当者が優先すべき対応アクションを3件、日本語で簡潔に提示してください。

【評価データ】
{vendor_summary}

【回答形式】
1. [具体的な対応アクション] → [期待効果・根拠]
2. [具体的な対応アクション] → [期待効果・根拠]
3. [具体的な対応アクション] → [期待効果・根拠]

EU CRA・経産省ガイドラインの観点も踏まえて、実施優先度が高い順に提案してください。"""


def analyze_vendors(vendor_scores: List[Dict]) -> List[str]:
    client = anthropic.Anthropic()

    summary_lines = []
    for vs in vendor_scores:
        axes = vs.get('axes', {})
        issues = []
        for ax in ['sbom', 'questionnaire', 'incident_history']:
            issues.extend(axes.get(ax, {}).get('issues', []))
        issue_text = ', '.join(issues[:3]) if issues else '問題なし'
        summary_lines.append(
            f"  {vs.get('vendor', '不明')}: グレード{vs['grade']} ({vs['total']}点) — {issue_text}"
        )

    prompt = VENDOR_ANALYSIS_PROMPT.format(
        vendor_summary='\n'.join(summary_lines)
    )

    response = client.messages.create(
        model='claude-sonnet-4-6',
        max_tokens=500,
        messages=[{'role': 'user', 'content': prompt}],
    )

    lines = response.content[0].text.strip().split('\n')
    return [line.strip() for line in lines if line.strip()]

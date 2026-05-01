from typing import Dict, List

WEIGHTS = {
    'sbom':             0.45,
    'questionnaire':    0.35,
    'incident_history': 0.20,
}

GRADES = [(90, 'S'), (80, 'A'), (70, 'B'), (60, 'C'), (50, 'D'), (0, 'E')]


def score_sbom(data: Dict) -> Dict:
    score = 100
    issues: List[str] = []

    if data.get('sbom_missing'):
        score -= 30
        issues.append('SBOMが提出されていません（EU CRA要件未充足）')

    critical = data.get('critical_cves', 0)
    if critical > 0:
        score -= min(critical * 25, 50)
        issues.append(f'CRITICAL CVE検出: {critical}件（即時パッチ適用が必要）')

    high = data.get('high_cves', 0)
    if high > 0:
        score -= min(high * 10, 30)
        issues.append(f'HIGH CVE検出: {high}件')

    return {'score': max(0, score), 'issues': issues}


def score_questionnaire(data: Dict) -> Dict:
    score = 100
    issues: List[str] = []

    answered = data.get('answered', 0)
    total = data.get('total', 1)
    response_rate = answered / total if total > 0 else 0

    if response_rate < 1.0:
        deduct = round((1.0 - response_rate) * 30)
        score -= deduct
        issues.append(f'アンケート回答率が低い: {response_rate * 100:.0f}%（{answered}/{total}問）')

    pass_rate = data.get('pass_rate', 1.0)
    if pass_rate < 0.8:
        deduct = round((0.8 - pass_rate) * 100)
        score -= deduct
        issues.append(f'セキュリティ基準の適合率が低い: {pass_rate * 100:.0f}%')

    return {'score': max(0, score), 'issues': issues}


def score_incident_history(data: Dict) -> Dict:
    score = 100
    issues: List[str] = []

    if data.get('breach_history', False):
        score -= 40
        issues.append('過去にセキュリティ侵害の履歴があります')

    incidents = data.get('incidents_12m', 0)
    if incidents > 0:
        score -= min(incidents * 15, 30)
        issues.append(f'直近12ヶ月のインシデント: {incidents}件')

    return {'score': max(0, score), 'issues': issues}


def calculate_vendor_score(axes: Dict) -> Dict:
    total = sum(
        axes[axis]['score'] * weight
        for axis, weight in WEIGHTS.items()
        if axis in axes
    )
    total = round(total)

    grade = 'E'
    for threshold, g in GRADES:
        if total >= threshold:
            grade = g
            break

    return {'total': total, 'grade': grade}


def build_vendor_score(vendor_data: Dict) -> Dict:
    axes = {
        'sbom':             score_sbom(vendor_data.get('sbom', {})),
        'questionnaire':    score_questionnaire(vendor_data.get('questionnaire', {})),
        'incident_history': score_incident_history(vendor_data.get('incident_history', {})),
    }
    summary = calculate_vendor_score(axes)
    return {**summary, 'axes': axes, 'vendor': vendor_data.get('vendor', '不明')}

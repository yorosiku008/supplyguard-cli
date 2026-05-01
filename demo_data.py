from typing import List, Dict


def get_demo_scores() -> List[Dict]:
    from scorer import build_vendor_score

    vendors = [
        {
            'vendor': 'Alpha製造株式会社',
            'sbom': {'components': ['openssl-1.1.1', 'log4j-2.14.0'], 'critical_cves': 1, 'high_cves': 2, 'total_cves': 3},
            'questionnaire': {'answered': 8, 'total': 10, 'pass_rate': 0.75},
            'incident_history': {'incidents_12m': 0, 'breach_history': False},
        },
        {
            'vendor': 'Beta Systems Ltd.',
            'sbom': {'components': ['nginx-1.20', 'python-3.9'], 'critical_cves': 0, 'high_cves': 1, 'total_cves': 1},
            'questionnaire': {'answered': 10, 'total': 10, 'pass_rate': 0.9},
            'incident_history': {'incidents_12m': 0, 'breach_history': False},
        },
        {
            'vendor': 'Gamma Tech Partners',
            'sbom': {'components': [], 'critical_cves': 0, 'high_cves': 0, 'total_cves': 0, 'sbom_missing': True},
            'questionnaire': {'answered': 4, 'total': 10, 'pass_rate': 0.5},
            'incident_history': {'incidents_12m': 2, 'breach_history': True},
        },
    ]

    return [build_vendor_score(v) for v in vendors]

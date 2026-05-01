import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ── score_sbom ────────────────────────────────────────────

def test_score_sbom_returns_dict():
    from scorer import score_sbom
    result = score_sbom({'components': [], 'critical_cves': 0, 'high_cves': 0, 'total_cves': 0})
    assert isinstance(result, dict)
    assert 'score' in result
    assert 'issues' in result


def test_score_sbom_no_vulnerabilities_is_perfect():
    from scorer import score_sbom
    result = score_sbom({'components': ['libssl'], 'critical_cves': 0, 'high_cves': 0, 'total_cves': 0})
    assert result['score'] == 100


def test_score_sbom_critical_cve_reduces_score():
    from scorer import score_sbom
    result = score_sbom({'components': ['log4j'], 'critical_cves': 1, 'high_cves': 0, 'total_cves': 1})
    assert result['score'] < 100
    assert len(result['issues']) > 0


def test_score_sbom_high_cve_reduces_score():
    from scorer import score_sbom
    result = score_sbom({'components': ['openssl'], 'critical_cves': 0, 'high_cves': 2, 'total_cves': 2})
    assert result['score'] < 100


def test_score_sbom_no_sbom_reduces_score():
    from scorer import score_sbom
    result = score_sbom({'components': [], 'critical_cves': 0, 'high_cves': 0, 'total_cves': 0, 'sbom_missing': True})
    assert result['score'] <= 70
    assert len(result['issues']) > 0


# ── score_questionnaire ───────────────────────────────────

def test_score_questionnaire_returns_dict():
    from scorer import score_questionnaire
    result = score_questionnaire({'answered': 10, 'total': 10, 'pass_rate': 1.0})
    assert isinstance(result, dict)
    assert 'score' in result


def test_score_questionnaire_full_pass_is_perfect():
    from scorer import score_questionnaire
    result = score_questionnaire({'answered': 10, 'total': 10, 'pass_rate': 1.0})
    assert result['score'] == 100


def test_score_questionnaire_low_pass_rate_reduces_score():
    from scorer import score_questionnaire
    result = score_questionnaire({'answered': 10, 'total': 10, 'pass_rate': 0.4})
    assert result['score'] < 70


def test_score_questionnaire_unanswered_reduces_score():
    from scorer import score_questionnaire
    result = score_questionnaire({'answered': 5, 'total': 10, 'pass_rate': 1.0})
    assert result['score'] < 100


# ── score_incident_history ────────────────────────────────

def test_score_incident_history_returns_dict():
    from scorer import score_incident_history
    result = score_incident_history({'incidents_12m': 0, 'breach_history': False})
    assert isinstance(result, dict)
    assert 'score' in result


def test_score_incident_history_no_incidents_is_perfect():
    from scorer import score_incident_history
    result = score_incident_history({'incidents_12m': 0, 'breach_history': False})
    assert result['score'] == 100


def test_score_incident_history_recent_breach_reduces_score():
    from scorer import score_incident_history
    result = score_incident_history({'incidents_12m': 2, 'breach_history': True})
    assert result['score'] <= 40


# ── calculate_vendor_score ────────────────────────────────

def test_calculate_vendor_score_returns_dict():
    from scorer import calculate_vendor_score
    axes = {
        'sbom': {'score': 80, 'issues': []},
        'questionnaire': {'score': 75, 'issues': []},
        'incident_history': {'score': 90, 'issues': []},
    }
    result = calculate_vendor_score(axes)
    assert 'total' in result
    assert 'grade' in result


def test_calculate_vendor_score_all_perfect_is_s():
    from scorer import calculate_vendor_score
    axes = {k: {'score': 100, 'issues': []} for k in ['sbom', 'questionnaire', 'incident_history']}
    result = calculate_vendor_score(axes)
    assert result['total'] == 100
    assert result['grade'] == 'S'


def test_calculate_vendor_score_grade_b():
    from scorer import calculate_vendor_score
    axes = {k: {'score': 75, 'issues': []} for k in ['sbom', 'questionnaire', 'incident_history']}
    result = calculate_vendor_score(axes)
    assert result['grade'] == 'B'


def test_calculate_vendor_score_grade_d():
    from scorer import calculate_vendor_score
    axes = {k: {'score': 55, 'issues': []} for k in ['sbom', 'questionnaire', 'incident_history']}
    result = calculate_vendor_score(axes)
    assert result['grade'] == 'D'

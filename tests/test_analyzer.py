import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import MagicMock, patch

SAMPLE_VENDOR_SCORES = [
    {
        'vendor': 'Alpha製造株式会社',
        'total': 76,
        'grade': 'B',
        'axes': {
            'sbom': {'score': 55, 'issues': ['CRITICAL CVE検出: 1件']},
            'questionnaire': {'score': 89, 'issues': []},
            'incident_history': {'score': 100, 'issues': []},
        },
    },
    {
        'vendor': 'Gamma Tech Partners',
        'total': 56,
        'grade': 'D',
        'axes': {
            'sbom': {'score': 70, 'issues': ['SBOMが提出されていません']},
            'questionnaire': {'score': 52, 'issues': ['回答率40%']},
            'incident_history': {'score': 30, 'issues': ['侵害履歴あり']},
        },
    },
]


def make_mock_response(text: str):
    mock_content = MagicMock()
    mock_content.text = text
    mock_response = MagicMock()
    mock_response.content = [mock_content]
    return mock_response


@patch('analyzer.anthropic.Anthropic')
def test_analyze_vendors_returns_list(mock_cls):
    mock_client = MagicMock()
    mock_cls.return_value = mock_client
    mock_client.messages.create.return_value = make_mock_response(
        "1. Alpha製造にCRITICAL CVEの修正期限を設定してください\n"
        "2. Gamma Techへのアンケート再送を実施してください\n"
        "3. SBOM未提出ベンダーへの提出義務化を検討してください"
    )
    from analyzer import analyze_vendors
    result = analyze_vendors(SAMPLE_VENDOR_SCORES)
    assert isinstance(result, list)
    assert len(result) >= 1


@patch('analyzer.anthropic.Anthropic')
def test_analyze_vendors_returns_strings(mock_cls):
    mock_client = MagicMock()
    mock_cls.return_value = mock_client
    mock_client.messages.create.return_value = make_mock_response("1. 提案A\n2. 提案B")
    from analyzer import analyze_vendors
    result = analyze_vendors(SAMPLE_VENDOR_SCORES)
    for item in result:
        assert isinstance(item, str) and len(item) > 0


@patch('analyzer.anthropic.Anthropic')
def test_analyze_vendors_calls_claude(mock_cls):
    mock_client = MagicMock()
    mock_cls.return_value = mock_client
    mock_client.messages.create.return_value = make_mock_response("1. 提案")
    from analyzer import analyze_vendors
    analyze_vendors(SAMPLE_VENDOR_SCORES)
    mock_client.messages.create.assert_called_once()
    kwargs = mock_client.messages.create.call_args[1]
    assert kwargs['model'] == 'claude-sonnet-4-6'


@patch('analyzer.anthropic.Anthropic')
def test_analyze_vendors_prompt_includes_vendor_name(mock_cls):
    mock_client = MagicMock()
    mock_cls.return_value = mock_client
    mock_client.messages.create.return_value = make_mock_response("1. 提案")
    from analyzer import analyze_vendors
    analyze_vendors(SAMPLE_VENDOR_SCORES)
    kwargs = mock_client.messages.create.call_args[1]
    prompt = kwargs['messages'][0]['content']
    assert 'Alpha' in prompt or 'Gamma' in prompt

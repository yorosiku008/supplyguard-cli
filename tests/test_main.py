import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import patch, MagicMock


def test_parse_args_defaults():
    from main import parse_args
    args = parse_args([])
    assert args.demo is False
    assert args.vendor is None
    assert args.output_md is False


def test_parse_args_demo_flag():
    from main import parse_args
    args = parse_args(['--demo'])
    assert args.demo is True


def test_parse_args_vendor():
    from main import parse_args
    args = parse_args(['--vendor', 'ACME Corp'])
    assert args.vendor == 'ACME Corp'


def test_parse_args_output_md():
    from main import parse_args
    args = parse_args(['--output-md'])
    assert args.output_md is True


def test_run_demo_mode_uses_demo_data():
    from main import run
    with patch('main.get_demo_scores') as mock_demo, \
         patch('main.print_report') as mock_print:
        mock_demo.return_value = [{'vendor': 'Demo社', 'total': 60, 'grade': 'C', 'axes': {}}]
        run(demo=True)
        mock_demo.assert_called_once()
        mock_print.assert_called_once()


def test_run_saves_md_when_flag_set():
    from main import run
    with patch('main.get_demo_scores') as mock_demo, \
         patch('main.print_report'), \
         patch('main.build_md_report') as mock_build, \
         patch('main.save_md_report') as mock_save:
        mock_demo.return_value = [{'vendor': 'Demo社', 'total': 60, 'grade': 'C', 'axes': {}}]
        mock_build.return_value = '# report'
        run(demo=True, output_md=True)
        mock_save.assert_called_once()

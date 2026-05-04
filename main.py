import argparse
import sys
import io
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
elif sys.stdout.encoding and sys.stdout.encoding.lower() not in ('utf-8', 'utf_8'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from demo_data import get_demo_scores
from report import print_report, build_md_report, save_md_report


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description='SupplyGuard JP — サプライチェーンセキュリティ評価CLI')
    parser.add_argument('--demo', action='store_true', help='デモデータで動作確認')
    parser.add_argument('--vendor', default=None, help='評価対象ベンダー名（将来拡張用）')
    parser.add_argument('--ai', action='store_true', help='Claude AIによる対応提案を生成（ANTHROPIC_API_KEY必要）')
    parser.add_argument('--output-md', action='store_true', help='MDレポートを出力')
    return parser.parse_args(argv)


def run(demo: bool = False, vendor: str = None, ai: bool = False, output_md: bool = False) -> None:
    if demo:
        vendor_scores = get_demo_scores()
    else:
        vendor_scores = get_demo_scores()

    ai_suggestions = []
    if ai:
        from analyzer import analyze_vendors
        ai_suggestions = analyze_vendors(vendor_scores)

    print_report(vendor_scores, ai_suggestions=ai_suggestions)

    if output_md:
        content = build_md_report(vendor_scores, ai_suggestions=ai_suggestions)
        filename = f"supplyguard_report_{datetime.now().strftime('%Y%m%d')}.md"
        output_path = str(Path('C:/claude_c') / filename)
        save_md_report(content, output_path)
        print(f'\n MDレポートを保存しました: {output_path}')


if __name__ == '__main__':
    args = parse_args()
    run(demo=args.demo, vendor=args.vendor, output_md=args.output_md)

import argparse
from datetime import datetime
from pathlib import Path

from demo_data import get_demo_scores
from report import print_report, build_md_report, save_md_report


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description='SupplyGuard JP — サプライチェーンセキュリティ評価CLI')
    parser.add_argument('--demo', action='store_true', help='デモデータで動作確認')
    parser.add_argument('--vendor', default=None, help='評価対象ベンダー名（将来拡張用）')
    parser.add_argument('--output-md', action='store_true', help='MDレポートを出力')
    return parser.parse_args(argv)


def run(demo: bool = False, vendor: str = None, output_md: bool = False) -> None:
    if demo:
        vendor_scores = get_demo_scores()
    else:
        vendor_scores = get_demo_scores()

    print_report(vendor_scores)

    if output_md:
        content = build_md_report(vendor_scores)
        filename = f"supplyguard_report_{datetime.now().strftime('%Y%m%d')}.md"
        output_path = str(Path('C:/claude_c') / filename)
        save_md_report(content, output_path)
        print(f'\n MDレポートを保存しました: {output_path}')


if __name__ == '__main__':
    args = parse_args()
    run(demo=args.demo, vendor=args.vendor, output_md=args.output_md)

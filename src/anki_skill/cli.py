"""CLI entry point for anki-export."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from anki_skill.exporters import export_apkg, export_tsv
from anki_skill.parser import parse_cards


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="anki-export",
        description="Parse pipe-delimited flashcards and export to Anki formats.",
    )
    parser.add_argument(
        "input",
        help="Input file with pipe-delimited cards, or '-' for stdin.",
    )
    parser.add_argument(
        "-f", "--format",
        choices=["tsv", "apkg"],
        default="tsv",
        help="Output format (default: tsv).",
    )
    parser.add_argument(
        "-o", "--output",
        required=True,
        help="Output file path.",
    )
    parser.add_argument(
        "-d", "--deck-name",
        default="AnkiSkill Export",
        help="Deck name for APKG export (default: 'AnkiSkill Export').",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show skipped lines and additional details.",
    )

    args = parser.parse_args(argv)

    if args.input == "-":
        text = sys.stdin.read()
    else:
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"Error: file not found: {args.input}", file=sys.stderr)
            sys.exit(1)
        text = input_path.read_text(encoding="utf-8-sig")

    cards = parse_cards(text, verbose=args.verbose)

    if not cards:
        print("Error: no cards parsed from input.", file=sys.stderr)
        sys.exit(2)

    output_path = Path(args.output)
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print(f"Error: cannot create output directory: {e}", file=sys.stderr)
        sys.exit(3)

    try:
        if args.format == "tsv":
            export_tsv(cards, output_path)
        else:
            export_apkg(cards, output_path, deck_name=args.deck_name)
    except OSError as e:
        print(f"Error: cannot write output file: {e}", file=sys.stderr)
        sys.exit(3)

    print(f"Exported {len(cards)} cards to {output_path}", file=sys.stderr)


if __name__ == "__main__":
    main()

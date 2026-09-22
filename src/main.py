import argparse, json, logging
from pathlib import Path
from .workflow import process

def main():
    parser = argparse.ArgumentParser(description="AI × X運用支援PoC")
    parser.add_argument("input_json", type=Path)
    parser.add_argument("--output", type=Path, default=Path("output/result.json"))
    parser.add_argument("--log", type=Path, default=Path("output/run.log"))
    args = parser.parse_args()

    args.log.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[logging.FileHandler(args.log, encoding="utf-8"), logging.StreamHandler()],
        force=True,
    )

    with args.input_json.open("r", encoding="utf-8") as f:
        data = json.load(f)

    result = process(data)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result.to_dict(), ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    logging.info(
        "処理完了 theme=%s revision=%s human_review=%s",
        result.theme,
        result.revision_required,
        result.human_review_required,
    )

    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

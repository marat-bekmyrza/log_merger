import json

import time
import argparse
from pathlib import Path
from datetime import datetime


_LOG_FILENAMES = 'log_a.jsonl', 'log_b.jsonl'
_OUT_FILENAME = 'log_merged.jsonl'


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Tool to merge two logs.')

    parser.add_argument(
        'log1_dir',
        metavar='<LOG1 DIR>',
        type=str,
        help='path to dir with log1 file',
    )

    parser.add_argument(
        'log2_dir',
        metavar='<LOG2 DIR>',
        type=str,
        help='path to dir with log2 file',
    )

    parser.add_argument(
        '-o',
        type=str,
        default='./',
        help='path to dir for output file',
        dest='out_dir'
    )

    return parser.parse_args()


def _get_logs_filepath(log1_dir: Path, log2_dir: Path) -> (Path, Path):
    log1_filename, log2_filename = _LOG_FILENAMES
    log1_path = log1_dir.joinpath(log1_filename)
    log2_path = log2_dir.joinpath(log2_filename)

    if not log1_path.exists():
        raise FileNotFoundError(f'File "{log1_path}" doesn\'t exist')
    if not log2_path.exists():
        raise FileNotFoundError(f'File "{log2_path}" doesn\'t exist')

    return log1_path, log2_path


def _get_out_filepath(out_dir: Path) -> Path:
    if not out_dir.exists():
        out_dir.mkdir(parents=True)
    return out_dir.joinpath(_OUT_FILENAME)


def _merge_logs(log1_path: Path, log2_path: Path, out_path: Path) -> None:
    log1_file, log2_file = open(log1_path, 'r'), open(log2_path, 'r')
    out_file = open(out_path, 'w')

    log1_lines, log2_lines = log1_file.readlines(), log2_file.readlines()
    counter1, counter2 = 0, 0

    while counter1 < len(log1_lines) and counter2 < len(log2_lines):
        line1, line2 = log1_lines[counter1], log2_lines[counter2]
        line1_json = json.loads(line1)
        line2_json = json.loads(line2)

        line1_time = datetime.strptime(line1_json['timestamp'], '%Y-%m-%d %H:%M:%S')
        line2_time = datetime.strptime(line2_json['timestamp'], '%Y-%m-%d %H:%M:%S')

        if line1_time < line2_time:
            data = line1
            counter1 += 1
        else:
            data = line2
            counter2 += 1
        out_file.write(data)

    while counter1 < len(log1_lines):  # remaining from the log1
        data = log1_lines[counter1]
        out_file.write(data)
        counter1 += 1

    while counter2 < len(log2_lines):  # remaining from the log2
        data = log2_lines[counter2]
        out_file.write(data)
        counter2 += 1

    log1_file.close()
    log2_file.close()
    out_file.close()


def main() -> None:
    args = _parse_args()
    t0 = time.time()

    log1_dir, log2_dir = Path(args.log1_dir), Path(args.log2_dir)
    output_dir = Path(args.out_dir)

    log1_path, log2_path = _get_logs_filepath(log1_dir, log2_dir)
    out_path = _get_out_filepath(output_dir)
    _merge_logs(log1_path, log2_path, out_path)

    print(f"finished in {time.time() - t0:0f} sec")


if __name__ == '__main__':
    main()

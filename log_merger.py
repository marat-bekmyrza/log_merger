import json

import time
import argparse
import dataclasses
import random
import shutil

from datetime import datetime, timedelta
from pathlib import Path


_LOG_FILENAMES = 'log_a.jsonl', 'log_b.jsonl'
_OUT_FILENAME = 'log_merged.jsonl'


@dataclasses.dataclass
class LogRecord:
    log_level: str
    timestamp: str
    message: str


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Tool to merge two logs.')

    parser.add_argument(
        'log1_dir',
        metavar='<LOG1 PATH>',
        type=str,
        help='path to log1 file',
    )

    parser.add_argument(
        'log2_dir',
        metavar='<LOG2 PATH>',
        type=str,
        help='path to log2 file',
    )

    parser.add_argument(
        '-o',
        type=str,
        default='./',
        help='path for output file',
        dest='out_dir'
    )

    return parser.parse_args()


def _create_out_dir(dir_path: Path) -> None:
    if not dir_path.exists():
        dir_path.mkdir(parents=True)

#
# _RECORD_TEMPLATE = LogRecord(
#     log_level='<LOG_LEVEL>',
#     timestamp='<TIMESTAMP>',
#     message='<MESSAGE>',
# )
#
# _MESSAGE_TEMPLATE = json.dumps(dataclasses.asdict(_RECORD_TEMPLATE)).encode('utf-8')
# _MESSAGE_TEMPLATE += b'\n'
#
#
# def _generate_logfile(log_filepath: Path, start_time: datetime) -> None:
#     print(f"generating {log_filepath.name}...")
#     person_name, action = _PERSON_NAME, _ACTION
#     object, place, when = _OBJECT, _PLACE, _WHEN
#     log_levels, message_template = _LOG_LEVELS, _MESSAGE_TEMPLATE
#     rand, td, ln = random.random, timedelta, len
#
#     with log_filepath.open('wb') as fh:
#         current_time = start_time
#         total_size, max_size = 0, _MAX_LOG_SIZE_BYTES
#         write = fh.write
#         while total_size < max_size:
#             timestamp = f"{current_time.year}-{current_time.month:02}-{current_time.day:02} " \
#                         f"{current_time.hour}:{current_time.minute:02}:{current_time.second:02}".encode('utf-8')
#
#             message = f"{person_name[int(6 * rand())]} " \
#                       f"{action[int(10 * rand())]} " \
#                       f"{object[int(8 * rand())]} " \
#                       f"{place[int(4 * rand())]} " \
#                       f"{when[int(5 * rand())]}".encode('utf-8')
#
#             data = message_template \
#                 .replace(b'<LOG_LEVEL>', log_levels[int(4 * rand())]) \
#                 .replace(b'<TIMESTAMP>', timestamp) \
#                 .replace(b'<MESSAGE>', message)
#
#             write(data)
#             total_size += ln(data)
#             current_time += td(seconds=int(10 * rand()))
#
#
# def _merge_logs(output_dir: Path) -> None:
#     start_time = datetime.now()
#
#     for log_filename in _LOG_FILENAMES:
#         log_path = output_dir.joinpath(log_filename)
#         _generate_logfile(log_path, start_time)


def main() -> None:
    args = _parse_args()

    t0 = time.time()
    log1_dir, log2_dir = Path(args.log1_dir), Path(args.log2_dir)
    output_dir = Path(args.out_dir)
    _create_out_dir(output_dir)
    # _merge_logs(log1_dir, log2_dir)
    print(f"finished in {time.time() - t0:0f} sec")


if __name__ == '__main__':
    main()

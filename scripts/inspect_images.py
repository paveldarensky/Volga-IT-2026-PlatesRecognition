"""Просмотр изображений из папки.
Стрелки ← → — листать, Delete — удалить, Q / Esc — выход.
"""
import argparse
from pathlib import Path

import cv2

EXTS = {".jpg", ".jpeg", ".png"}


def collect_images(folder: Path) -> list[Path]:
    return sorted(p for p in folder.iterdir() if p.suffix.lower() in EXTS)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder", type=Path)
    args = ap.parse_args()

    files = collect_images(args.folder)
    if not files:
        print(f"нет изображений в {args.folder}")
        return

    idx = 0
    while 0 <= idx < len(files):
        path = files[idx]
        img = cv2.imread(str(path))
        if img is None:
            print(f"не прочиталось: {path.name}")
            idx += 1
            continue

        # ресайз под экран, если большое
        h, w = img.shape[:2]
        if w > 1280:
            scale = 1280 / w
            img = cv2.resize(img, (1280, int(h * scale)))

        title = f"[{idx + 1}/{len(files)}] {path.name}"
        cv2.imshow(title, img)
        key = cv2.waitKey(0) & 0xFF

        cv2.destroyAllWindows()

        if key in (ord("q"), 27):        # q / Esc
            break
        elif key == 81 or key == 2:      # ←
            idx = max(0, idx - 1)
        elif key == 83 or key == 3:      # →
            idx = min(len(files) - 1, idx + 1)
        elif key == 255 or key == 8:     # Delete / Backspace
            print(f"удаляю {path.name}")
            path.unlink()
            files.pop(idx)
        else:
            idx += 1


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse
import json
import os
from pathlib import Path


def default_project_root() -> Path:
    env_root = os.environ.get("NOVEL_PROJECT_ROOT")
    if env_root:
        return Path(env_root)
    return Path(__file__).resolve().parents[1] / "assets" / "sample-novel-project"


def default_reviewed_chapters_dir() -> Path | None:
    env_root = os.environ.get("NOVEL_REVIEWED_CHAPTERS_DIR")
    if env_root:
        return Path(env_root)
    repo_candidate = Path(__file__).resolve().parents[3] / "人工二次审核过后的正文"
    if repo_candidate.exists():
        return repo_candidate
    return None


def chapter_filename(chapter: int) -> str:
    return f"chapter-{chapter:04d}.txt"


def chapter_outline_filename(chapter: int) -> str:
    return f"chapter-{chapter:04d}-outline.md"


def effective_chapter_path(chapters_dir: Path, chapter: int, reviewed_dir: Path | None) -> Path | None:
    filename = chapter_filename(chapter)
    if reviewed_dir:
        reviewed_candidate = reviewed_dir / filename
        if reviewed_candidate.exists():
            return reviewed_candidate
    project_candidate = chapters_dir / filename
    if project_candidate.exists():
        return project_candidate
    return None


def list_existing_chapters(chapters_dir: Path, reviewed_dir: Path | None = None) -> list[Path]:
    names = {path.name for path in chapters_dir.glob("chapter-*.txt")}
    if reviewed_dir:
        names.update(path.name for path in reviewed_dir.glob("chapter-*.txt"))
    existing: list[Path] = []
    for name in sorted(names):
        chapter = int(name.removeprefix("chapter-").removesuffix(".txt"))
        candidate = effective_chapter_path(chapters_dir, chapter, reviewed_dir)
        if candidate:
            existing.append(candidate)
    return existing


def find_recent_previous(
    chapters_dir: Path,
    chapter: int,
    reviewed_dir: Path | None = None,
    limit: int = 3,
) -> list[Path]:
    recent: list[Path] = []
    for idx in range(chapter - 1, 0, -1):
        candidate = effective_chapter_path(chapters_dir, idx, reviewed_dir)
        if candidate:
            recent.append(candidate)
            if len(recent) >= limit:
                break
    return recent


def ensure_project(project_root: Path) -> None:
    (project_root / "chapters").mkdir(parents=True, exist_ok=True)
    (project_root / "outlines").mkdir(parents=True, exist_ok=True)
    (project_root / "tracking").mkdir(parents=True, exist_ok=True)


def build_context(mode: str, chapter: int, project_root: Path) -> dict:
    ensure_project(project_root)
    chapters_dir = project_root / "chapters"
    outlines_dir = project_root / "outlines"
    tracking_dir = project_root / "tracking"
    reviewed_dir = default_reviewed_chapters_dir()
    current_chapter_file = chapters_dir / chapter_filename(chapter)
    current_chapter_source = effective_chapter_path(chapters_dir, chapter, reviewed_dir)
    recent_previous = find_recent_previous(chapters_dir, chapter, reviewed_dir)
    total_outline_file = outlines_dir / "chapter-outlines.md"
    split_outline_file = outlines_dir / chapter_outline_filename(chapter)
    existing_chapters = list_existing_chapters(chapters_dir, reviewed_dir)

    return {
        "mode": mode,
        "chapter": chapter,
        "project_root": str(project_root.resolve()),
        "chapters_dir": str(chapters_dir.resolve()),
        "reviewed_chapters_dir": str(reviewed_dir.resolve()) if reviewed_dir else "",
        "reviewed_chapters_exists": bool(reviewed_dir and reviewed_dir.exists()),
        "overlay_active": bool(reviewed_dir and reviewed_dir.exists()),
        "outlines_dir": str(outlines_dir.resolve()),
        "tracking_dir": str(tracking_dir.resolve()),
        "current_chapter_file": str(current_chapter_file.resolve()),
        "current_chapter_exists": current_chapter_file.exists(),
        "current_chapter_source_file": str(current_chapter_source.resolve()) if current_chapter_source else "",
        "current_chapter_source_exists": bool(current_chapter_source),
        "latest_previous_chapter_file": str(recent_previous[0].resolve()) if recent_previous else "",
        "latest_previous_exists": bool(recent_previous),
        "recent_previous_chapter_files": [str(path.resolve()) for path in recent_previous],
        "existing_chapter_files": [str(path.resolve()) for path in existing_chapters],
        "latest_existing_chapter_file": str(existing_chapters[-1].resolve()) if existing_chapters else "",
        "total_outline_file": str(total_outline_file.resolve()),
        "total_outline_exists": total_outline_file.exists(),
        "split_outline_file": str(split_outline_file.resolve()),
        "split_outline_exists": split_outline_file.exists(),
        "missing_outline_hint": not total_outline_file.exists() and not split_outline_file.exists(),
        "foreshadows_file": str((tracking_dir / "foreshadows.md").resolve()),
        "foreshadows_exists": (tracking_dir / "foreshadows.md").exists(),
        "timeline_file": str((tracking_dir / "timeline.md").resolve()),
        "timeline_exists": (tracking_dir / "timeline.md").exists(),
        "character_status_file": str((tracking_dir / "character-status.md").resolve()),
        "character_status_exists": (tracking_dir / "character-status.md").exists(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="小说章节上下文辅助脚本")
    parser.add_argument("mode", choices=["chapter", "outline"])
    parser.add_argument("--chapter", type=int, required=True)
    parser.add_argument(
        "--project-root",
        default=str(default_project_root()),
        help="小说工程根目录。默认使用共享 sample-novel-project，也可用 NOVEL_PROJECT_ROOT 覆盖。",
    )
    args = parser.parse_args()

    context = build_context(args.mode, args.chapter, Path(args.project_root))
    print(json.dumps(context, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

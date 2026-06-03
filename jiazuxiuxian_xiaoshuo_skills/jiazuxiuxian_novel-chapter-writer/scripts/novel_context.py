#!/usr/bin/env python3
import argparse
import json
import os
import re
from pathlib import Path


BOOK_PLAN_NAME = "《家族修仙：这一脉，由我来立》小说策划案.md"
TRACKING_FILENAMES = ("上下文.md", "伏笔.md", "时间线.md", "角色状态.md")


def default_project_root() -> Path:
    env_root = os.environ.get("NOVEL_PROJECT_ROOT")
    if env_root:
        return Path(env_root)
    return Path(__file__).resolve().parents[1] / "assets" / "sample-novel-project"


def default_master_plan_file() -> Path:
    env_file = os.environ.get("NOVEL_MASTER_PLAN_FILE")
    if env_file:
        return Path(env_file)
    return Path(__file__).resolve().parents[3] / BOOK_PLAN_NAME


def default_reviewed_chapters_dir(project_root: Path) -> Path | None:
    env_root = os.environ.get("NOVEL_REVIEWED_CHAPTERS_DIR")
    if env_root:
        return Path(env_root)
    for candidate_name in ("正文_人工二审", "人工二次审核过后的正文"):
        candidate = project_root / candidate_name
        if candidate.exists():
            return candidate
    return None


def chapter_prefix(chapter: int) -> str:
    return f"第{chapter:03d}章"


def chapter_filename(chapter: int, title: str = "待定") -> str:
    return f"{chapter_prefix(chapter)}_{title}.md"


def chapter_outline_prefix(chapter: int) -> str:
    return f"细纲_第{chapter:03d}章"


def chapter_outline_filename(chapter: int) -> str:
    return f"{chapter_outline_prefix(chapter)}.md"


def find_matching_file(directory: Path, prefix: str) -> Path | None:
    if not directory.exists():
        return None
    matches = sorted(path for path in directory.glob(f"{prefix}*.md") if path.is_file())
    return matches[0] if matches else None


def effective_chapter_path(chapters_dir: Path, chapter: int, reviewed_dir: Path | None) -> Path | None:
    prefix = chapter_prefix(chapter)
    if reviewed_dir:
        reviewed_candidate = find_matching_file(reviewed_dir, prefix)
        if reviewed_candidate:
            return reviewed_candidate
    return find_matching_file(chapters_dir, prefix)


def list_markdown_files(directory: Path, pattern: str = "*.md") -> list[Path]:
    if not directory.exists():
        return []
    return sorted(path.resolve() for path in directory.glob(pattern) if path.is_file())


def existing_chapter_numbers(chapters_dir: Path, reviewed_dir: Path | None = None) -> list[int]:
    numbers: set[int] = set()
    pattern = re.compile(r"^第(\d{3})章")
    for directory in filter(None, [chapters_dir, reviewed_dir]):
        if not directory or not directory.exists():
            continue
        for path in directory.glob("第*章*.md"):
            match = pattern.match(path.name)
            if match:
                numbers.add(int(match.group(1)))
    return sorted(numbers)


def list_existing_chapters(chapters_dir: Path, reviewed_dir: Path | None = None) -> list[Path]:
    existing: list[Path] = []
    for number in existing_chapter_numbers(chapters_dir, reviewed_dir):
        candidate = effective_chapter_path(chapters_dir, number, reviewed_dir)
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
    for relative in [
        "设定/世界观",
        "设定/角色",
        "设定/势力",
        "大纲",
        "正文",
        "追踪",
        "参考资料",
    ]:
        (project_root / relative).mkdir(parents=True, exist_ok=True)


def build_context(mode: str, project_root: Path, chapter: int | None = None) -> dict:
    ensure_project(project_root)
    settings_dir = project_root / "设定"
    worldview_dir = settings_dir / "世界观"
    characters_dir = settings_dir / "角色"
    factions_dir = settings_dir / "势力"
    outlines_dir = project_root / "大纲"
    chapters_dir = project_root / "正文"
    tracking_dir = project_root / "追踪"
    research_dir = project_root / "参考资料"
    reviewed_dir = default_reviewed_chapters_dir(project_root)
    master_plan_file = default_master_plan_file()

    existing_chapters = list_existing_chapters(chapters_dir, reviewed_dir)
    total_outline_file = outlines_dir / "大纲.md"
    volume_outline_files = sorted(path.resolve() for path in outlines_dir.glob("卷纲_*.md"))
    outline_files = list_markdown_files(outlines_dir, "细纲_第*.md")
    worldview_files = list_markdown_files(worldview_dir)
    character_files = list_markdown_files(characters_dir)
    faction_files = list_markdown_files(factions_dir)

    relation_file = settings_dir / "关系.md"
    genre_positioning_file = settings_dir / "题材定位.md"
    naming_reserve_file = settings_dir / "命名储备.md"
    context_file = tracking_dir / "上下文.md"
    foreshadows_file = tracking_dir / "伏笔.md"
    timeline_file = tracking_dir / "时间线.md"
    character_status_file = tracking_dir / "角色状态.md"
    post_action_update_files = [
        str(context_file.resolve()),
        str(foreshadows_file.resolve()),
        str(timeline_file.resolve()),
        str(character_status_file.resolve()),
    ]

    current_chapter_file = None
    current_chapter_source = None
    current_chapter_outline_file = None
    current_chapter_outline_source = None
    recent_previous: list[Path] = []

    if chapter is not None:
        current_chapter_file = chapters_dir / chapter_filename(chapter)
        current_chapter_source = effective_chapter_path(chapters_dir, chapter, reviewed_dir)
        current_chapter_outline_file = outlines_dir / chapter_outline_filename(chapter)
        current_chapter_outline_source = find_matching_file(outlines_dir, chapter_outline_prefix(chapter))
        recent_previous = find_recent_previous(chapters_dir, chapter, reviewed_dir)

    return {
        "mode": mode,
        "chapter": chapter,
        "project_root": str(project_root.resolve()),
        "settings_dir": str(settings_dir.resolve()),
        "worldview_dir": str(worldview_dir.resolve()),
        "characters_dir": str(characters_dir.resolve()),
        "factions_dir": str(factions_dir.resolve()),
        "relation_file": str(relation_file.resolve()),
        "relation_exists": relation_file.exists(),
        "genre_positioning_file": str(genre_positioning_file.resolve()),
        "genre_positioning_exists": genre_positioning_file.exists(),
        "naming_reserve_file": str(naming_reserve_file.resolve()),
        "naming_reserve_exists": naming_reserve_file.exists(),
        "outlines_dir": str(outlines_dir.resolve()),
        "chapters_dir": str(chapters_dir.resolve()),
        "tracking_dir": str(tracking_dir.resolve()),
        "research_dir": str(research_dir.resolve()),
        "reviewed_chapters_dir": str(reviewed_dir.resolve()) if reviewed_dir else "",
        "reviewed_chapters_exists": bool(reviewed_dir and reviewed_dir.exists()),
        "overlay_active": bool(reviewed_dir and reviewed_dir.exists()),
        "master_plan_file": str(master_plan_file.resolve()),
        "master_plan_exists": master_plan_file.exists(),
        "current_chapter_file": str(current_chapter_file.resolve()) if current_chapter_file else "",
        "current_chapter_exists": bool(current_chapter_file and current_chapter_file.exists()),
        "current_chapter_source_file": str(current_chapter_source.resolve()) if current_chapter_source else "",
        "current_chapter_source_exists": bool(current_chapter_source),
        "current_chapter_outline_file": str(current_chapter_outline_file.resolve()) if current_chapter_outline_file else "",
        "current_chapter_outline_exists": bool(
            (current_chapter_outline_file and current_chapter_outline_file.exists()) or current_chapter_outline_source
        ),
        "current_chapter_outline_source_file": str(current_chapter_outline_source.resolve()) if current_chapter_outline_source else "",
        "latest_previous_chapter_file": str(recent_previous[0].resolve()) if recent_previous else "",
        "latest_previous_exists": bool(recent_previous),
        "recent_previous_chapter_files": [str(path.resolve()) for path in recent_previous],
        "existing_chapter_files": [str(path.resolve()) for path in existing_chapters],
        "latest_existing_chapter_file": str(existing_chapters[-1].resolve()) if existing_chapters else "",
        "total_outline_file": str(total_outline_file.resolve()),
        "total_outline_exists": total_outline_file.exists(),
        "volume_outline_files": [str(path) for path in volume_outline_files],
        "volume_outline_exists": bool(volume_outline_files),
        "outline_files": [str(path) for path in outline_files],
        "worldview_files": [str(path) for path in worldview_files],
        "character_files": [str(path) for path in character_files],
        "faction_files": [str(path) for path in faction_files],
        "missing_outline_hint": bool(
            chapter is not None
            and not total_outline_file.exists()
            and not volume_outline_files
            and not current_chapter_outline_source
        ),
        "context_file": str(context_file.resolve()),
        "context_exists": context_file.exists(),
        "foreshadows_file": str(foreshadows_file.resolve()),
        "foreshadows_exists": foreshadows_file.exists(),
        "timeline_file": str(timeline_file.resolve()),
        "timeline_exists": timeline_file.exists(),
        "character_status_file": str(character_status_file.resolve()),
        "character_status_exists": character_status_file.exists(),
        "post_action_update_required": True,
        "post_action_update_files": post_action_update_files,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="仙侠家族小说统一写作上下文辅助脚本")
    parser.add_argument("mode", choices=["chapter", "outline", "setting"])
    parser.add_argument("--chapter", type=int, help="章节号；chapter/outline 模式必填。")
    parser.add_argument(
        "--project-root",
        default=str(default_project_root()),
        help="小说工程根目录。默认使用 sample-novel-project，也可用 NOVEL_PROJECT_ROOT 覆盖。",
    )
    args = parser.parse_args()

    if args.mode in {"chapter", "outline"} and args.chapter is None:
        parser.error("--chapter is required for chapter/outline mode")

    context = build_context(args.mode, Path(args.project_root), args.chapter)
    print(json.dumps(context, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

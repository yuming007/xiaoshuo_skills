#!/usr/bin/env node

const pkg = require("random_chinese_fantasy_names");

const RARITY_SCORE = {
  common: 0,
  uncommon: 1,
  rare: 2,
  epic: 3,
  legendary: 4,
  mythic: 5,
  exotic: 6,
};

const BANNED_GLOBAL = [
  "少林",
  "武当",
  "峨眉",
  "华山",
  "嵩山",
  "崆峒",
  "青城",
  "蜀山",
];

const BANNED_GRAND = [
  "诛仙",
  "灭世",
  "万劫",
  "无极",
  "太古",
  "洪荒",
  "诸天",
  "九天",
  "魔神",
  "修罗",
  "黄泉",
  "轮回",
  "霸天",
  "无上",
];

const BANNED_NAME_CHARS = [
  "萌",
  "蝶",
  "舞",
  "妖",
  "媚",
  "娇",
  "艳",
  "霸",
  "魔",
  "邪",
  "煞",
  "屠",
  "灭",
  "帝",
  "霞",
  "绮",
  "瑛",
  "莹",
  "玥",
  "霏",
  "窈",
  "橙",
  "咏",
  "邦",
  "德",
  "四",
  "千",
];

const BANNED_NAME_WORDS = ["宝宝", "甜甜", "依依"];

const BANNED_SKILL_WORDS = [
  "老虎",
  "天兵",
  "勾魂",
  "吸星",
  "屠龙",
  "诛仙",
  "灭世",
  "霸王",
  "无敌",
  "如来",
];

const DESIRED_NAME_CHARS = [
  "清",
  "承",
  "青",
  "衡",
  "岳",
  "川",
  "宁",
  "芷",
  "岚",
  "澄",
  "庭",
  "岩",
  "行",
  "舟",
  "砚",
  "观",
  "玄",
  "照",
  "渊",
  "礼",
  "慎",
  "修",
  "归",
  "守",
  "和",
  "谦",
  "临",
  "修",
  "安",
  "朔",
  "宁",
];

const DESIRED_FACTION_WORDS = [
  "河",
  "泉",
  "石",
  "岭",
  "桥",
  "渡",
  "工",
  "渠",
  "仓",
  "契",
  "潮",
  "岚",
  "青",
  "东",
  "临",
  "归",
  "汀",
  "梁",
  "坊",
  "观",
  "院",
  "社",
  "会",
  "阁",
  "盟",
];

const DESIRED_LOCATION_WORDS = [
  "河",
  "岭",
  "湾",
  "渡",
  "潭",
  "谷",
  "汀",
  "石",
  "潮",
  "岚",
  "青",
  "月",
  "云",
  "照",
  "归",
  "听",
  "桥",
  "梁",
];

const DESIRED_SKILL_WORDS = [
  "导",
  "引",
  "养",
  "脉",
  "泉",
  "气",
  "炁",
  "息",
  "神",
  "阵",
  "符",
  "御",
  "理",
  "藏",
  "稳",
  "清",
  "归",
];

function parseArgs(argv) {
  const args = {
    type: "name",
    count: 10,
    family: "",
    style: "",
    female: false,
    kind: "",
    prefix: "",
    postfix: "",
    length: 0,
    attempts: 8,
    overGenerate: 5,
  };

  for (let i = 2; i < argv.length; i += 1) {
    const a = argv[i];
    if (a === "--type") args.type = argv[++i];
    else if (a === "--count") args.count = Number(argv[++i]);
    else if (a === "--family") args.family = argv[++i];
    else if (a === "--style") args.style = argv[++i];
    else if (a === "--female") args.female = true;
    else if (a === "--kind") args.kind = argv[++i];
    else if (a === "--prefix") args.prefix = argv[++i];
    else if (a === "--postfix") args.postfix = argv[++i];
    else if (a === "--length") args.length = Number(argv[++i]);
    else if (a === "--attempts") args.attempts = Number(argv[++i]);
    else if (a === "--over-generate") args.overGenerate = Number(argv[++i]);
  }
  return args;
}

function includesAny(text, items) {
  return items.some((item) => text.includes(item));
}

function scoreByWords(text, words) {
  let score = 0;
  for (const word of words) {
    if (text.includes(word)) score += 1;
  }
  return score;
}

function rawGenerate(type, count, args) {
  switch (type) {
    case "name":
      return pkg.getName(count, {
        isFemale: args.female || undefined,
        style: args.style || undefined,
        familyName: args.family || undefined,
      }).map((name) => ({ name }));
    case "dao":
      return pkg.getDao(count, {
        isFemale: args.female || undefined,
        title: args.kind || undefined,
        firstCharacter: args.prefix || undefined,
      });
    case "skill":
      return pkg.getSkill(count, {
        length: args.length || undefined,
        kind: args.kind || undefined,
        prefix: args.prefix || undefined,
        numfix: args.postfix || undefined,
      });
    case "book":
      return pkg.getBook(count, {
        length: args.length || undefined,
        prefix: args.prefix || undefined,
        mainkind: args.kind || undefined,
        postfix: args.postfix || undefined,
      });
    case "clan":
      return pkg.getClan(count, args.kind || undefined).map((name) => ({ name }));
    case "nation":
      return pkg.getNation(count, args.kind || undefined);
    case "location":
      return pkg.getLocation(count, args.kind || undefined);
    case "zone":
      return pkg.getZone(count, args.kind || undefined);
    default:
      throw new Error(`unsupported type: ${type}`);
  }
}

function rejectByGlobal(text) {
  return includesAny(text, BANNED_GLOBAL) || includesAny(text, BANNED_GRAND);
}

function evaluateName(item, args) {
  const text = item.name;
  if (rejectByGlobal(text)) return null;
  if (includesAny(text, BANNED_NAME_WORDS)) return null;
  if ([...text].some((ch) => BANNED_NAME_CHARS.includes(ch))) return null;
  if (args.family && !text.startsWith(args.family)) return null;
  if (args.family && text.length !== args.family.length + 2) return null;
  if (!args.family && (text.length < 2 || text.length > 4)) return null;
  if (/[0-9一二三四五六七八九十百千]/.test(text)) return null;
  if (includesAny(text, ["轩辕", "诸葛", "夏侯", "澹台", "欧阳", "长孙", "司徒", "上官"])) return null;

  let score = 0;
  if (args.family && text.length === args.family.length + 2) score += 3;
  if (!text.includes("轩辕") && !text.includes("夏侯") && !text.includes("诸葛")) score += 1;
  score += scoreByWords(text, DESIRED_NAME_CHARS);
  if (args.female && includesAny(text, ["清", "宁", "岚", "芷", "澄", "禾", "素"])) score += 2;
  if (!args.female && includesAny(text, ["承", "青", "衡", "岳", "川", "庭", "岩", "行", "舟", "礼"])) score += 2;
  if (!args.female && includesAny(text, ["华", "勇", "勋", "濯", "鹏", "煊", "仕", "旗"])) score -= 1;
  if (args.female && includesAny(text, ["梦", "彩", "晴", "舒", "竹"])) score -= 1;
  if (score < 4) return null;
  return { ...item, score };
}

function evaluateClan(item, args) {
  const text = item.name;
  if (rejectByGlobal(text)) return null;
  if (text.length > 6) return null;
  if (args.kind && !text.endsWith(args.kind)) return null;
  if (includesAny(text, ["勾魂", "血魔", "大力", "霸王", "白虎", "朱雀", "青龙", "玄武", "百兽", "伏虎", "伏龙", "封仙", "荡魔"])) return null;

  let score = 0;
  score += scoreByWords(text, DESIRED_FACTION_WORDS);
  if (includesAny(text, ["社", "会", "院", "坊", "阁", "盟", "观", "堂"])) score += 2;
  if (includesAny(text, ["宗", "宫", "神教"])) score -= 1;
  if (score < 3) return null;
  return { ...item, score };
}

function evaluateLocation(item, args) {
  const text = item.name;
  if (rejectByGlobal(text)) return null;
  if (args.kind && !text.endsWith(args.kind)) return null;
  if (text.length < 2 || text.length > 5) return null;
  if (["前", "后", "左", "右", "上", "下"].includes(text[0])) return null;
  if (includesAny(text, ["百魔", "苍狼", "达摩", "丹熏"])) return null;

  let score = 0;
  score += scoreByWords(text, DESIRED_LOCATION_WORDS);
  if (includesAny(text, ["岭", "河", "湾", "渡", "潭", "谷", "池", "崖", "关"])) score += 2;
  if (score < 3) return null;
  return { ...item, score };
}

function evaluateSkill(item, args) {
  const text = item.name;
  if (rejectByGlobal(text)) return null;
  if (includesAny(text, BANNED_SKILL_WORDS)) return null;
  if (text.length < 3 || text.length > 8) return null;
  if (args.kind && !text.endsWith(args.kind)) return null;
  if (/[一二三四五六七八九十百千]/.test(text) && text.length > 6) return null;
  if (includesAny(text, ["毒龙", "百鬼", "雌雄", "白云火焰", "诛龙"])) return null;

  let score = 0;
  score += scoreByWords(text, DESIRED_SKILL_WORDS);
  if (includesAny(text, ["诀", "术", "法", "篇"])) score += 2;
  if (text.length <= 5) score += 2;
  if (text.length >= 7) score -= 1;
  if (score < 4) return null;
  return { ...item, score };
}

function evaluateBook(item) {
  const text = item.name;
  if (rejectByGlobal(text)) return null;
  if (text.length < 3 || text.length > 8) return null;
  let score = 0;
  score += scoreByWords(text, DESIRED_SKILL_WORDS);
  if (includesAny(text, ["经", "典", "篇", "图"])) score += 2;
  if (score < 3) return null;
  return { ...item, score };
}

function evaluateNationOrZone(item) {
  const text = item.name;
  if (rejectByGlobal(text)) return null;
  let score = 0;
  score += (RARITY_SCORE[item.rarity] || 0);
  score += scoreByWords(text, DESIRED_LOCATION_WORDS);
  return { ...item, score };
}

function evaluate(type, item, args) {
  switch (type) {
    case "name":
    case "dao":
      return evaluateName(item, args);
    case "clan":
      return evaluateClan(item, args);
    case "location":
      return evaluateLocation(item, args);
    case "skill":
      return evaluateSkill(item, args);
    case "book":
      return evaluateBook(item, args);
    case "nation":
    case "zone":
      return evaluateNationOrZone(item);
    default:
      return item;
  }
}

function main() {
  const args = parseArgs(process.argv);
  const target = args.count;
  const pool = new Map();

  for (let i = 0; i < args.attempts; i += 1) {
    const rawCount = Math.max(target * args.overGenerate, target);
    const batch = rawGenerate(args.type, rawCount, args);
    for (const item of batch) {
      const judged = evaluate(args.type, item, args);
      if (!judged) continue;
      const prev = pool.get(judged.name);
      if (!prev || judged.score > prev.score) pool.set(judged.name, judged);
    }
    if (pool.size >= target * 2) break;
  }

  const items = [...pool.values()]
    .sort((a, b) => {
      if (b.score !== a.score) return b.score - a.score;
      return a.name.localeCompare(b.name, "zh-Hans-CN");
    })
    .slice(0, target);

  process.stdout.write(`${JSON.stringify(items, null, 2)}\n`);
}

main();

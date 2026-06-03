#!/usr/bin/env node

const pkg = require("random_chinese_fantasy_names");

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
  }
  return args;
}

function uniq(items, keyFn = (x) => x) {
  const seen = new Set();
  const out = [];
  for (const item of items) {
    const key = keyFn(item);
    if (seen.has(key)) continue;
    seen.add(key);
    out.push(item);
  }
  return out;
}

function output(items) {
  process.stdout.write(`${JSON.stringify(items, null, 2)}\n`);
}

function buildName(args) {
  return uniq(
    pkg.getName(args.count, {
      isFemale: args.female || undefined,
      style: args.style || undefined,
      familyName: args.family || undefined,
    })
  );
}

function buildDao(args) {
  return uniq(
    pkg.getDao(args.count, {
      isFemale: args.female || undefined,
      title: args.kind || undefined,
      firstCharacter: args.prefix || undefined,
    }),
    (x) => x.name
  );
}

function buildSkill(args) {
  return uniq(
    pkg.getSkill(args.count, {
      length: args.length || undefined,
      kind: args.kind || undefined,
      prefix: args.prefix || undefined,
      numfix: args.postfix || undefined,
    }),
    (x) => x.name
  );
}

function buildBook(args) {
  return uniq(
    pkg.getBook(args.count, {
      length: args.length || undefined,
      prefix: args.prefix || undefined,
      mainkind: args.kind || undefined,
      postfix: args.postfix || undefined,
    }),
    (x) => x.name
  );
}

function buildClan(args) {
  return uniq(pkg.getClan(args.count, args.kind || undefined));
}

function buildNation(args) {
  return uniq(pkg.getNation(args.count, args.kind || undefined), (x) => x.name);
}

function buildLocation(args) {
  return uniq(pkg.getLocation(args.count, args.kind || undefined), (x) => x.name);
}

function buildZone(args) {
  return uniq(pkg.getZone(args.count, args.kind || undefined), (x) => x.name);
}

function main() {
  const args = parseArgs(process.argv);
  switch (args.type) {
    case "name":
      output(buildName(args));
      return;
    case "dao":
      output(buildDao(args));
      return;
    case "skill":
      output(buildSkill(args));
      return;
    case "book":
      output(buildBook(args));
      return;
    case "clan":
      output(buildClan(args));
      return;
    case "nation":
      output(buildNation(args));
      return;
    case "location":
      output(buildLocation(args));
      return;
    case "zone":
      output(buildZone(args));
      return;
    default:
      throw new Error(`unsupported type: ${args.type}`);
  }
}

main();

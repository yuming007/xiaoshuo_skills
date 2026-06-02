---
name: novel-outline-planner
description: 生成长篇历史小说章节大纲的中文技能。用于用户要求“生成第 N 章大纲”“补第 N 章章纲”“规划下一章或后续几章”时调用。技能默认读取共享小说工程中的已写章节、当前剧情状态、总设定与已有章纲，并将新大纲写入 chapter-outlines.md。适合连载规划、补全断档章纲、根据前文修正后续走向，并默认为单章约 4000 字正文提供足够材料。
---

# 小说章节大纲

## 默认工程

除非用户明确指定别的小说工程目录，否则一律使用共享默认工程：

`skills/novel-chapter-writer/assets/sample-novel-project/`

不要要求用户手动同步两套目录。正文 skill 与大纲 skill 默认共用这一套工程。

## 用户常见说法

- 生成第 7 章大纲
- 根据前六章补第 8 章章纲
- 规划第 7 章到第 10 章
- 重做第 6 章后的后续走向

## 信息优先级

遇到冲突时，严格按下面优先级处理：

1. 小说工程里的已写正文
2. 小说工程里的现有章纲
3. `references/current-story-state.md`
4. `../novel-chapter-writer/references/characters/` 里的相关人物档案
5. `references/novel-bible.md`
6. `../novel-chapter-writer/references/naturalness-rules.md`
7. 一般性历史常识与默认推断

已成稿正文始终高于旧卷纲和旧设定。

## 工作流程

### 1. 先定位上下文

先运行：

```bash
python3 scripts/novel_context.py outline --chapter N
```

脚本默认会指向共享小说工程，并返回：

- 当前章对应的大纲文件信息
- 最近一章正文
- 最近三章正文列表
- 总大纲文件位置
- 当前工程根目录

### 2. 先读哪些文件

生成章纲前，按下面顺序读取：

1. `references/current-story-state.md`
2. 小说工程内的 `outlines/chapter-outlines.md`
3. `../novel-chapter-writer/references/characters/index.md`
4. 读取本章相关人物档案，至少包括主角和最近一章核心出场人物
5. `references/novel-bible.md`
6. `../novel-chapter-writer/references/naturalness-rules.md`
7. `../novel-chapter-writer/references/qidian-editor-rules.md`
8. `../novel-chapter-writer/references/qidian-opening-patterns.md`
9. 按任务性质补读共享专项模块：
   - 默认至少读 `../novel-chapter-writer/references/modules/volume_outline/runtime.md`
   - 当前章冲突、因果或阻力偏弱时，补读 `../novel-chapter-writer/references/modules/plot_logic/runtime.md`
   - 章末牵引偏弱时，补读 `../novel-chapter-writer/references/modules/chapter_ending/runtime.md`
   - 当前章与上一章承接紧时，补读 `../novel-chapter-writer/references/modules/transition/runtime.md`
   - 多人物并行或关系续接复杂时，补读 `../novel-chapter-writer/references/modules/character_consistency/runtime.md`
10. 最近一章正文
11. 如该章承接紧密，再补读最近两到三章正文

### 3. 大纲必须解决什么

每一章的大纲都要解决四件事：

- 这一章承接了什么
- 这一章真正推进了什么
- 这一章制造了什么新的阻力或代价
- 这一章结尾把读者推向哪一章

不要只写主题词，不要只写人物情绪。

同时注意：

- 场景安排不要写得过满，给正文留出自然发挥空间
- 不要提前替正文把“道理”讲完，否则落地后容易满篇模板腔
- 每章尽量包含“当章事务、当章阻力、部分兑现、章末钩子”四个要素
- 历史读者偏重逻辑和情怀，章纲里的冲突必须合身份、合制度、合时代处境

### 3.1 与正文体量的匹配

除非用户明确要求短章或大章，否则默认按单章约 4000 字正文倒推章纲密度。

- 当前章通常准备 3 到 5 个有效场景，或 2 个大场景加 1 到 2 个过渡场景
- 每个场景都要有明确目标、动作变化或关系变化，不能只写情绪和判断
- 章纲过薄会逼得正文注水，章纲过满会把正文挤成流水账
- 因此章纲既要有足够材料撑起约 4000 字，也要给正文留下自然展开空间

### 3.2 起点开局规则

本 skill 默认按起点历史频道的追读逻辑做章纲。

这不是用户额外提出时才开启的附加选项，而是默认规则：

- 始终受 `../novel-chapter-writer/references/qidian-editor-rules.md` 约束
- 始终参考 `../novel-chapter-writer/references/qidian-opening-patterns.md`
- 即使不是前三章，也默认保留“快入事、强事务、强牵引”的平台节奏

如果处理的是第1章到第3章，或某一卷的卷首章，必须严格满足下面分工：

- 第1章：异变、危机、穿越落地、身份反差至少要出现两项，先把读者拉进场
- 第2章：快速落身份、关系、生存环境，用具体场景补信息
- 第3章：让主角做出第一轮明确决断，并推出下一阶段路径

不要把前三章都写成设定说明书。开局章纲必须先解决“读者为什么继续看”。

如果处理的是第4章以后：

- 不要生搬前三章模板
- 但仍默认要求每章有当章事务、明确阻力、部分兑现、章末钩子
- 仍默认要求开头尽快入事，避免空转

### 3.3 大纲组织规则

- 总路线要写到足够远，但细节采用前详后略
- 当前章到接下来三章，应写得足够细，方便正文直接落地
- 更远处的走向，只要写清方向、阶段冲突与预期转折即可
- 不要为了求新奇硬造大量陌生名词，优先使用读者容易理解的说法

### 3.4 专项模块默认接入

本 skill 现在默认吸收共享专项模块的结构化检查，不再只靠经验判断。

最低要求：

- 用 `volume_outline/runtime.md` 检查本章是不是有“目标、阻力、变化、章末拉力”
- 用 `plot_logic/runtime.md` 检查本章冲突是不是合因果，不是作者硬推
- 用 `chapter_ending/runtime.md` 检查章末是否真能把人推向下一章

按需要补充：

- 若本章紧接上一章余波，补用 `transition/runtime.md`
- 若本章涉及多人物关系续接，补用 `character_consistency/runtime.md`

### 4. 大纲格式

优先使用下面格式，确保正文 skill 可直接拿来写：

```markdown
## 第7章 章名

- 本章定位：
- 本章即时看点：
- 核心冲突：
- 承接前文：
- 推进结果：
- 本章兑现：

### 场景一
- 地点：
- 出场人物：
- 场景目标：
- 关键事件：
- 结果：

### 场景二
...

- 本章伏笔回收：
- 本章新伏笔：
- 章末钩子：
```

### 5. 当前连续性硬约束

补后续章纲时必须承认以下既成事实：

- 当前故事起步时间是延熹十年，现进度推进到熹平元年
- 贾诩已经完成从凉州家中蛰伏到入洛出仕的第一阶段转折
- 主角已与马腾结识，并已进入杨赐、杨元所主导的郎署与南掖门体系
- 第6章到第9章当前采用重构路线：围绕凉州边报、军饷封事与门簿程序展开士宦暗斗
- “法不可弃，锋不可露”应作为这一组四章阶段收束后的结果，而不是预设成已发生事实

### 6. 落盘规则

默认写入：

`outlines/chapter-outlines.md`

处理原则：

- 已有该章大纲：整体替换该章小节
- 没有该章大纲：追加到文件末尾
- 用户要求连续生成多章：按顺序一次性追加多个章节小节

如新章纲明显改变后续路线，还应同步修订：

- `references/current-story-state.md`
- 相关人物档案

### 7. 质量闸门

章纲不能首稿直接落盘。必须执行：

1. 先完成一版章纲草稿
2. 按下面清单逐条自检
3. 只要有硬性条件不满足，就重做对应场景或整章结构
4. 直到满足要求后，才允许写入最终文件

自检执行顺序：

1. 先过 `../novel-chapter-writer/references/modules/volume_outline/runtime.md`
2. 再过 `../novel-chapter-writer/references/modules/plot_logic/runtime.md`
3. 再过 `../novel-chapter-writer/references/modules/chapter_ending/runtime.md`
4. 如承接紧或人物复杂，再补过 `transition/runtime.md`、`character_consistency/runtime.md`

章纲自检清单：

- 是否与已写正文、现有人物档案、当前剧情状态冲突
- 是否写清了这一章承接什么、推进什么、制造什么阻力、把人推向哪一章
- 是否存在明确“当章事务”，而不只是主题和情绪
- 场景密度是否足以支撑约 4000 字正文，又不至于拥挤到像流水账
- 冲突是否合身份、合制度、合时代，不是生造麻烦
- 场景是否够具体，能支撑正文直接展开
- 是否包含“本章即时看点、本章兑现、章末钩子”
- 是否默认体现了起点历史频道的追读节奏，而不是只有在用户点名时才启用
- 若为第1章到第3章或卷首章，是否严格满足起点开局分工
- 是否前详后略，没有把远期剧情写死到失去弹性
- 是否避免把“道理”提前说尽，给正文留出发挥空间
- 是否已经按共享模块规则检查过：
  - 本章目标、阻力、变化、章末拉力
  - 动机、触发、后果是否成立
  - 章末是否能被下一章第一拍接住

重写规则：

- 轻微不合格：补字段、补冲突、补钩子
- 中度不合格：重排场景、重定推进结果
- 重度不合格：整章章纲推翻重做

只要自检后仍有硬伤，不得直接落盘。

## 输出要求

完成后只需简要说明：

- 生成了哪一章或哪几章的大纲
- 保存到了哪个文件
- 是否发现与前文冲突并已如何处理

## 参考文件

- `references/current-story-state.md`
- `../novel-chapter-writer/references/characters/`
- `references/novel-bible.md`
- `../novel-chapter-writer/references/naturalness-rules.md`
- `../novel-chapter-writer/references/qidian-editor-rules.md`
- `../novel-chapter-writer/references/qidian-opening-patterns.md`
- `../novel-chapter-writer/references/modules/README.md`
- `../novel-chapter-writer/references/modules/volume_outline/runtime.md`
- `../novel-chapter-writer/references/modules/plot_logic/runtime.md`
- `../novel-chapter-writer/references/modules/chapter_ending/runtime.md`
- `../novel-chapter-writer/references/modules/transition/runtime.md`
- `../novel-chapter-writer/references/modules/character_consistency/runtime.md`
- `references/chapter-outlines.md`
- `../novel-skills-tutorial.md`

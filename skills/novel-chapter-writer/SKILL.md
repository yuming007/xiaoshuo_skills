---
name: novel-chapter-writer
description: 生成长篇历史小说章节正文的中文技能。用于用户要求“写第 N 章”“续写第 N 章”“重写某章正文”时调用。技能默认读取共享小说工程中的已写章节、章节大纲、当前剧情状态和总设定，并将新正文保存到对应的 chapter-XXXX.txt 文件。适合持续连载、按既有文风续写、保持前后文一致，默认单章产出约 4000 字。
---

# 小说正文生成

## 默认工程

除非用户明确指定别的小说工程目录，否则一律使用默认共享工程：

`skills/novel-chapter-writer/assets/sample-novel-project/`

不要反复要求用户配置路径。当前项目里已经放入了前六章正文，默认直接基于这套内容继续写。

如果当前仓库根目录存在：

`人工二次审核过后的正文/`

则把它视为对 `sample-novel-project/chapters/` 的人工校正版覆盖层。

执行规则：

- 同章节号若两边都存在，一律优先读取人工二审稿
- 人工二审稿同时视为更高优先级的 canon 和更可靠的文风锚点
- 继续写新章时，默认仍写回工程内的 `chapters/`
- 只有用户明确要求时，才把新稿直接写进人工二审目录

该工程现在除 `chapters/` 与 `outlines/` 外，还默认支持：

- `tracking/foreshadows.md`
- `tracking/timeline.md`
- `tracking/character-status.md`

如果这些 tracking 文件存在，默认要读；如果不存在，不阻塞写作，但要退回正文与 `references/current-story-state.md` 自行推断。

## 用户常见说法

- 写第 7 章
- 续写第 8 章正文
- 重写第 6 章，让杨赐那场戏更有压迫感
- 根据现有设定和前文生成第 9 章

## 默认字数

除非用户明确指定更短或更长的字数目标，否则默认把单章正文控制在 4000 字左右。

执行口径：

- 默认目标区间为 3800 到 4300 字
- 非特殊情况不低于 3500 字，不高于 4500 字
- 低于 3500 字时，优先补足事务、阻力、兑现和章末牵引，不要靠空泛感慨硬拖
- 高于 4500 字时，优先压缩重复解释、合并弱场景，必要时把次要信息后移到下一章
- 如果用户明确要求“3000 字短章”“5000 字大章”或其他体量，以用户要求为准

## 信息优先级

遇到信息冲突时，严格按下面优先级处理：

1. `人工二次审核过后的正文/` 中存在的对应章节
2. 小说工程里的已写正文
3. 小说工程里的 `outlines/chapter-outlines.md`
4. `references/current-story-state.md`
5. `references/characters/` 里的相关人物档案
6. `references/novel-bible.md`
7. `references/naturalness-rules.md`
8. 一般性历史常识与默认推断

不要让参考设定反过来覆盖已成稿正文。

## 工作流程

### 1. 先定位上下文

先运行：

```bash
python3 scripts/novel_context.py chapter --chapter N
```

脚本默认会指向共享小说工程，并返回：

- 当前章输出文件
- 当前章优先读取的 source 文件
- 最近一章正文
- 最近三章正文列表
- 是否启用了人工二审正文覆盖层
- 大纲文件位置
- tracking 文件位置
- 当前工程根目录

### 2. 先读哪些文件

正文生成前，按下面顺序读取：

1. `references/current-story-state.md`
2. 小说工程内的 `outlines/chapter-outlines.md`
3. `references/characters/index.md`
4. 读取本章会出场的相关人物档案，至少包括主角与最近一章涉及的关键人物
5. `references/novel-bible.md`
6. `references/naturalness-rules.md`
7. `references/readability-rules.md`
8. `references/qidian-editor-rules.md`
9. `references/qidian-opening-patterns.md`
10. `references/tracking-protocol.md`
11. `references/history-hook-rules.md`
12. 如果当前仓库存在 `人工二次审核过后的正文/` 或本 skill 内存在 `references/manual-review-findings.md`，默认补读 `references/manual-review-findings.md`
13. 如果工程内存在 `tracking/foreshadows.md`、`tracking/timeline.md`、`tracking/character-status.md`，按当前章相关性抽读
14. 先整理一份“最简记忆包”，只保留本章写错风险最高的信息
15. 按任务性质补读共享专项模块：
   - 当前章章纲偏薄、阶段目标不清或需要回看章节结构时，补读 `references/modules/volume_outline/runtime.md`
   - 默认至少读 `references/modules/plot_logic/runtime.md`
   - 默认至少读 `references/modules/chapter_ending/runtime.md`
   - 完稿前必读 `references/modules/consistency_review/runtime.md`
   - 完稿前必读 `references/modules/anti_ai_voice/runtime.md`
   - 关系戏重时，补读 `references/modules/dialogue/runtime.md`
   - 与上一章承接紧时，补读 `references/modules/transition/runtime.md`
   - 人物状态复杂或跨章余波重时，补读 `references/modules/character_consistency/runtime.md`
16. 最近一章正文
17. 如当前章承接关系很强，再补读最近两到三章正文

如果当前章已有旧稿，必须先读旧稿，再决定是覆盖重写还是在原文基础上修订。

### 2.1 最简记忆包

开写前不要把全部信息平均带进正文。

必须先压成一份简短的“最简记忆包”，至少包含：

- 当前故事时间与当前处境
- 本章涉及人物的最新状态
- 本章相关伏笔
- 本章会受哪条程序、关系、时间约束

判断标准只有一条：

- 如果不知道这条信息，这一章就有较大概率写错，那就保留

和本章无关的设定、人物、远线伏笔不要硬塞进当前上下文。

### 3. 缺章纲时的处理

如果当前章没有明确章纲：

- 优先调用 `$novel-outline-planner` 先补大纲
- 如果用户就是要你直接写，也要先在心里生成一个简要场景提纲，再落正文

不要在毫无章纲和前文承接判断的情况下直接硬写。

### 3.1 续写与重写分流

如果用户说“续写第 N 章”：

- 先读旧稿
- 判断是接在旧稿末尾继续写，还是旧稿虽然存在但需要整章修
- 若旧稿已经形成完整章结构，但只差后半段，则优先接续
- 若旧稿方向、节奏、承接已经歪掉，不要硬续，改按重写处理

如果用户说“重写第 N 章”：

- 先读旧稿
- 必读前一章正文
- 若存在后一章，也必读后一章正文，避免重写后直接撞坏承接
- 重写后必须补查 `tracking/` 三件事：
  - 伏笔状态是否变化
  - 时间线是否变化
  - 角色状态是否变化

### 4. 正文写法

正文要承接当前前六章已经形成的剧情、人物关系和基本气质，但文面默认要往更顺口、更清楚、更像连载稿的方向校正，不要把前文里已经偏沉、偏密、偏正文腔的部分继续放大。

保持这些特征：

- 第三人称近距离视角，核心感知紧贴贾诩 / 商鞅
- 章节标题格式统一为“第X章 章名”
- 单章体量默认控制在 4000 字左右，场景数量与推进密度要足以撑起这个篇幅，但不要靠重复解释和空转硬凑字数
- 开头常用明确时间、地点、气候或场景锚点切入
- 开头第一拍优先落“谁在何处做什么”，不要先空写两三句气氛再把人物放进来
- 环境描写与内心复盘都要压量。能两三句交代清楚，就不要拖成整段；一旦开始讲道理，要尽快接回动作、对白或新信息
- 同一段里比喻尽量只留一个最有用的，不要一层动作再叠一层比喻、再补一层感慨
- 对话要体现试探、权衡、利害，而不是空泛喊口号
- 主角思考方式始终偏法家：先看权力、制度、利益、执行条件
- 文气可以沉稳、克制，但可读性优先。先保证读者一遍能读顺，再谈文气和质感
- 优先用常用词、明白句、短中句。不要为了显得厚重、古雅、深刻，故意写绕、写满、写得像策论
- 句式不要过分整齐，不要反复使用同一类排比、总结句、判断句
- 允许局部粗粝，宁可朴一点，也不要用力过猛地“写得像文学”
- 不要在动作或对白后再补一层作者点评，如“这话说得平平，反倒更重”“这不是X，更像Y”这类尾注句
- 人情味主要落在称呼、停顿、递东西、回头、避视、收手、改口等具体反应上，不靠整段煽情解释
- 结尾尽量用动作、场景余波、半句话头收住，而不是每章都用概括性总结句收束
- 不要把人物都写得很会说话，配角语言要带身份、局限和生活气
- 权谋感主要来自程序、责任链、称呼、站位、物证和留白，不来自大声讲道理
- 一段里优先只完成一项任务：交代现场、推进事务或点出判断。不要一段里景、情、理全挤满
- 调查、对簿、查证、审问类场景，压字时可以砍味道句，但不能砍掉证据链上的关键一环

### 4.1 平台节奏校准

本 skill 默认服务于起点男频历史频道取向。

这不是可选增强，而是默认工作模式：

- 始终受 `references/qidian-editor-rules.md` 约束
- 始终参考 `references/qidian-opening-patterns.md`
- 即使用户没有额外说明，也默认按“更像起点、更有追读感、开头更能抓人”的方向处理

如果用户明确说“不要平台化”“不要起点感太重”，才允许适度收掉部分平台节奏，但仍不能放弃“每章有事务、冲突推动、章末牵引”这些基本要求。

执行原则：

- 第一章先让事发生，再补设定
- 第二章先把身份和关系落稳，再补规则
- 第三章必须让主角做出第一轮明确动作
- 每章至少要有：当章事务、当章阻力、部分兑现、章末牵引
- 主角必须在具体处境里使用自己的优势，不能只在脑中高明
- 文字优先流畅直白，不堆辞藻，不玩现代梗
- 追读感主要来自问题清楚、事务推进和章末余力，不来自句子故作深沉
- 历史读者更看重合理与情怀，不要靠无脑打脸推进
- 你的书仍保持历史正剧底色，不改成轻佻爽文、不改成插科打诨腔

对当前这本已经写到第6章的小说：

- 第1章到第3章、卷首章、重写开篇时，严格执行 `references/qidian-opening-patterns.md`
- 第4章以后，不把前三章模板生搬硬套，但仍默认继承下面这些平台节奏：
  - 开头快入事
  - 每章有明确当章事务
  - 信息尽量压在场景、动作、对话里
  - 每章都有部分兑现
  - 章末留半步，把读者推向下一章

## 关于自然度与可读性

目标是写得更自然、更像连载稿，减少模板腔和明显机器感。

默认先满足一条：

- 普通网文读者第一次读时，基本不用回看句子，就能知道谁在做什么、这段话为什么要写

不要做的事：

- 不要为了“像小说”而每段都端着
- 不要为了“高级”而密集堆砌排比、长句、抽象判断
- 不要把简单意思故意写重、写古、写得半文半白
- 不要连续两到三段只靠气氛、心理、感慨撑住，而没有新动作、新信息、新对话
- 不要专门朝“规避检测”方向设计文本

要做的事：

- 多用常见词和直给句，先把意思说清
- 让信息落在人物、动作、场景和关系里
- 每一到两段至少给读者一个可见动作、对白或新信息
- 接受局部朴、局部粗、局部留白
- 保留前六章已经形成的自然节奏，但文面默认向更顺口、更易读校正，而不是机械继承前文的沉重句法

### 4.2 起点历史读者专项约束

- 历史频道读者对逻辑容忍度低，不能让关键人物为了配合主角而降智
- 情节应尽量做到“情理之中，意料之外”
- 本书主要爽感放在权、势、智、名与时代情怀，不走低俗擦边路线
- 一章里如果没有可见事务，只有复盘和感慨，要主动补一个现场问题或现实差事

### 4.3 专项模块默认链路

本 skill 现在默认吸收共享专项模块，不再只靠主提示词硬写。

开写前最低链路：

1. 用 `references/modules/plot_logic/runtime.md` 先写本章因果链
2. 用 `references/modules/character_consistency/runtime.md` 检查主角与关键人物状态是否接得上
3. 用 `references/modules/transition/runtime.md` 检查上一章余力怎样带进本章
4. 关系与冲突场景用 `references/modules/dialogue/runtime.md` 压对白
5. 本章收束前用 `references/modules/chapter_ending/runtime.md` 先定章末落点

文面修整顺序：

- 结构、人物、转场成立后，先用 `references/readability-rules.md` 做一次通顺度压缩，再用 `references/modules/anti_ai_voice/runtime.md` 做一次去模板腔和去 AI 味自检
- 如果当前仓库存在人工二审正文覆盖层，再额外用 `references/manual-review-findings.md` 对照一次，检查是否又写回“解释过满、比喻过密、尾注过多”的旧毛病

### 4.4 去 AI 味默认执行

本 skill 现在默认吸收 `story-deslop` 的有效部分，但已改造成历史权谋文口径。

默认不是“用户点名才处理”，而是正文完成后至少强制做一次 Gate 扫描：

- Gate A：高危词与高危句式
- Gate B：书面腔与策论腔
- Gate C：心理告知与重复拆写
- Gate D：节奏太平均
- Gate E：人物声音同质
- Gate F：章末总结体
- Gate G：晦涩与正文腔

处理原则：

- 只改表达，不改剧情功能
- 优先删掉套话，而不是换成另一句漂亮套话
- 章末一律避免“他不知道的是”“真正的风暴才刚开始”这一类空泛预告
- 历史文允许沉稳，但不允许滑、满、匀、假，也不允许句子故意拧着写

完稿后强制：

- 必须用 `references/modules/consistency_review/runtime.md` 过六检
- 任意两项不稳，不得直接落盘，必须回对应模块修

### 5. 当前连续性硬约束

续写时必须保持：

- 当前时间线在灵帝前期，不是董卓入京前夕
- 贾诩在本书里出身凉州士族兼将门，有父母、兄长、妻子与幼子
- 第四章已经与马腾相识
- 第五章已经通过光禄勋征辟入洛为郎中
- 第6章到第9章采用重构路线：旧版“南掖拦宦”正文不再视为有效 canon
- 这一阶段应围绕凉州边报、军饷封事、门簿底本与士宦暗斗推进
- “法不可弃，锋不可露”应作为第9章阶段收束后的结果，而不是开写时默认已完成的状态

### 6. 落盘规则

正文写入：

`chapters/chapter-XXXX.txt`

规则如下：

- 文件不存在：创建新文件
- 用户说“写第 N 章”：默认生成完整新章
- 用户说“续写第 N 章”：若已有文件，则在阅读旧稿后判断是接续还是整章修订
- 用户说“重写第 N 章”：整体覆盖原文件

如该章带来明显的新 canon 变化，完成正文后应同步更新：

- `references/current-story-state.md`
- 相关人物档案
- 工程内的 `tracking/foreshadows.md`
- 工程内的 `tracking/timeline.md`
- 工程内的 `tracking/character-status.md`

### 7. 质量闸门

正文不能首稿直接落盘。必须执行：

1. 先完成一版正文草稿
2. 按下面清单逐条自检，并粗查正文字符数
3. 只要有硬性条件不满足，就重写相关段落、场景甚至整章结构
4. 直到满足要求后，才允许写入最终文件

正文自检执行顺序：

1. 先按 `references/modules/consistency_review/runtime.md` 做六检
2. 有问题时回跳：
   - 逻辑问题 -> `references/modules/plot_logic/runtime.md`
   - 人物目标、情绪、关系、身体、声音问题 -> `references/modules/character_consistency/runtime.md`
   - 转场承接问题 -> `references/modules/transition/runtime.md`
   - 对白压力问题 -> `references/modules/dialogue/runtime.md`
   - 章末问题 -> `references/modules/chapter_ending/runtime.md`
3. 结构层通过后，再按 `references/modules/anti_ai_voice/runtime.md` 做文面去模板腔和去 AI 味检查
4. 再按 `references/readability-rules.md` 抽查三到五段，确认读者一遍能读顺
5. 若本次为续写或重写，再补查 tracking 是否需要回填

正文自检清单：

- 是否与已写正文、现有章纲、人物档案冲突
- 默认字数是否控制在 4000 字左右；若用户未另行指定，是否落在 3500 到 4500 字之间
- 是否承接了上一章至少一个明确问题或后果
- 是否存在当章事务，而不只是回忆、复盘、感慨
- 是否存在明确阻力，而不只是主角单向推进
- 主角是否通过行动、对话、判断推动了局面
- 关键人物是否符合身份、时代和既有性格，不存在降智配合
- 信息是否主要落在场景、动作、关系里，而不是大段解释
- 是否默认体现了起点历史频道的追读节奏，而不是只有在用户额外要求时才启用
- 文字是否流畅直白，是否存在明显模板腔、排比过多、总结句过多
- 是否存在需要回读才知道主语、宾语或因果关系的长句、绕句
- 是否存在简单意思被故意写重、写深、写得像正文点评或策论的地方
- 是否命中了明显高危 AI 句式，如“不是A，而是B”“……带着……”“他知道……”“他终于明白……”
- 是否存在同一瞬间被拆成两到三段反复写
- 是否连续两段以上没有新动作、新对白、新信息，只剩气氛、心理或判断
- 是否在对白或动作之后又补了一句作者代答式尾注，替读者总结轻重、寒意、杀机、人情
- 是否为了压缩篇幅，把关键证据链、情绪触发点或关系落点删断了
- 是否存在所有人物一个语气说话的问题
- 是否避免了明显现代网络词、玩梗式对白、轻佻爽文化爆发句
- 章末是否能把读者推向下一章，而不是用空洞总结收尾
- 若为第1章到第3章、卷首章或重写开篇，是否严格执行了 `references/qidian-opening-patterns.md`
- 是否已经按共享模块完成六检：
  - 剧情逻辑
  - 人物目标
  - 情绪关系
  - 身体信息
  - 场景转场
  - 章末承接
- 若 tracking 文件存在，是否已同步本章带来的伏笔、时间线、角色状态变化

重写规则：

- 轻微不合格：局部改写段落和对白，补足或压缩字数偏差
- 中度不合格：重排场景顺序，补事务、补阻力、补章末牵引
- 重度不合格：推翻草稿，按规则重写整章

只要自检后仍有硬伤，不得以“已经写完”为由直接交付。

## 输出要求

完成后只需简要说明：

- 写了哪一章
- 保存到了哪个文件
- 是否发现与前文或大纲冲突

## 参考文件

- `references/current-story-state.md`
- `references/characters/`
- `references/novel-bible.md`
- `references/naturalness-rules.md`
- `references/readability-rules.md`
- `references/manual-review-findings.md`
- `references/tracking-protocol.md`
- `references/history-hook-rules.md`
- `references/qidian-editor-rules.md`
- `references/qidian-opening-patterns.md`
- `references/modules/README.md`
- `references/modules/volume_outline/runtime.md`
- `references/modules/plot_logic/runtime.md`
- `references/modules/character_consistency/runtime.md`
- `references/modules/transition/runtime.md`
- `references/modules/dialogue/runtime.md`
- `references/modules/chapter_ending/runtime.md`
- `references/modules/anti_ai_voice/runtime.md`
- `references/modules/consistency_review/runtime.md`
- `references/chapter-outlines.md`
- `assets/sample-novel-project/`
- `../novel-skills-tutorial.md`

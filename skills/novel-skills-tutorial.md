# 小说 skills 使用教程

## 1. 现在的默认目录

两个 skill 默认共用这一套小说工程：

`C:\workspace_2\xiaoshuo_skills\skills\novel-chapter-writer\assets\sample-novel-project`

你已经把前六章正文放进了这里，所以现在属于零配置状态，可以直接用。

## 2. 目录里各文件是干什么的

- `chapters/`
  存放每章正文，例如 `chapter-0006.txt`
- `outlines/chapter-outlines.md`
  存放章节大纲总表
- `skills/novel-chapter-writer/references/characters/`
  存放人物档案，每个人物一个 md 文件
- `skills/novel-chapter-writer/references/novel-bible.md`
  存放总设定，也包含当前书名与简介

## 当前书名与简介

- 书名：《孤秦：商鞅重生三国》

简介：

商鞅车裂之后，重生成东汉少年贾诩。

此时汉室未崩，三国未起，洛阳却已暗流汹涌：宦官擅权，士族相争，边地将乱。

前世，他替秦国开路，最后却被清算；今生，他不想再走老路，只想先保自身，再借乱世往上走。

从凉州到洛阳，从家门到宫门，识马腾，见杨赐，避王甫，拒段颎。

这一世，他要换个活法。

## 3. 你平时怎么用

### 先生成大纲

直接说：

- `使用 $novel-outline-planner 生成第7章大纲`
- `使用 $novel-outline-planner 根据前六章规划第7章到第10章`

skill 会默认去读：

- 前六章正文
- 当前剧情状态
- 总设定
- 相关人物档案
- 现有章节大纲

然后把新大纲写回：

- `outlines/chapter-outlines.md`

### 再生成正文

直接说：

- `使用 $novel-chapter-writer 写第7章正文`
- `使用 $novel-chapter-writer 根据第7章大纲生成正文`

skill 会默认去读：

- 最新几章正文
- 当前剧情状态
- 总设定
- 相关人物档案
- `outlines/chapter-outlines.md` 里的对应章纲

然后把正文写到：

- `chapters/chapter-0007.txt`

默认情况下，`novel-chapter-writer` 会把单章正文控制在约 4000 字。

- 默认目标区间是 3800 到 4300 字
- 正常情况下不低于 3500 字，不高于 4500 字
- 如果你想要短章或大章，直接在指令里写明具体字数即可

## 4. 什么时候用哪个 skill

- 你还没有第 N 章章纲：先用 `novel-outline-planner`
- 你已经有第 N 章章纲：直接用 `novel-chapter-writer`
- 你觉得现有章纲不行：先让 `novel-outline-planner` 重做，再写正文
- 你觉得现有正文不行：直接让 `novel-chapter-writer` 重写该章

现在两个 skill 都不是“一次生成就结束”的模式了。

默认流程变成：

- 先生成草稿
- 再按规则自检
- 不合格就重写
- 直到满足条件才落盘

其中正文 skill 现在会额外检查：

- 是否达到了约 4000 字的默认体量
- 如果字数不足，是否是因为场景过薄、事务不够，而不是简单提前收尾
- 如果字数过长，是否存在重复解释、弱场景或应后移到下一章的信息

## 5. 常用说法示例

- `使用 $novel-outline-planner 生成第7章大纲，重点写杨赐召见后的余波。`
- `使用 $novel-chapter-writer 写第7章正文，延续前六章文风。`
- `使用 $novel-chapter-writer 写第7章正文，延续前六章文风，控制在4000字左右。`
- `使用 $novel-chapter-writer 重写第6章，让段颎的压迫感更强。`
- `使用 $novel-outline-planner 补全第7章到第9章的大纲，保持“法不可弃，锋不可露”的主线。`
- `使用 $novel-chapter-writer 写第7章正文，生成后按规则自检，不合格就继续重写到达标。`
- `使用 $novel-outline-planner 生成第8章大纲，先自检再落盘。`

## 6. 你不需要做的事

- 不需要手动给两个 skill 分别配路径
- 不需要手动执行脚本
- 不需要把同一份正文复制两份

这些步骤现在都已经收拢到默认工程里了。

## 7. 什么时候才需要额外配置

只有一种情况：你以后不想再用这个默认目录，而是想换到别的小说工程。

那时再告诉 skill：

- 新的小说工程根目录在哪里

除此之外，平时直接说“生成第 N 章大纲”或“写第 N 章正文”就行。

## 8. 人物档案怎么维护

人物档案统一放在：

`skills/novel-chapter-writer/references/characters/`

规则如下：

- 一个角色一个 md 文件
- 文件里写这个人物的生平记录、当前状态、与谁有关、说话做事的习惯
- 新人物正式进入正文后，最好立刻补一个人物文件
- 旧人物只要经历了重要事件，也要同步更新他的生平记录

这样两个 skill 在补大纲和写正文时，都会优先去读人物档案，而不是把人物信息散落在总设定里。

## 9. 起点节奏现在默认开启

我已经把一套“起点历史 / 秦汉三国方向常见有效开局规律”收进 skill 里，而且现在不是“你额外说了才启用”，而是默认就启用。

默认就会强化这些东西：

- 第一章更快入事，不先空讲背景
- 第二章更快落身份、关系、处境
- 第三章更快立目标、立路径、立下一步风险
- 每章都要有具体事务、具体阻力、部分兑现、章末钩子
- 第4章以后也默认保留追读节奏：开头快入事、信息压在场景里、章末留半步

这不等于把书改成套路爽文。

skill 仍然会保留：

- 历史正剧底色
- 克制文风
- 合时代、合身份、合权力逻辑
- 不靠无脑打脸推进

也就是说，现在默认目标就是：

- 更像起点历史频道
- 更有追读感
- 开局更像平台有效爆款写法
- 但不写成轻佻爽文

你如果还想额外加强，可以直接这样说：

- `使用 $novel-outline-planner 重做第1章到第3章大纲，按起点历史秦汉三国爆款开局节奏来做，但保留历史正剧底色。`
- `使用 $novel-chapter-writer 重写第1章，要求开场更快入事，先写车裂和魂穿，再补设定。`
- `使用 $novel-chapter-writer 写第7章正文，保留前六章文风，但把追读感再往上提。`

要注意：

- 第1章到第3章、卷首章、重写开篇时，会严格执行 `references/qidian-opening-patterns.md`
- 第4章以后，不会硬套前三章模板，但仍默认保留“开头快入事、信息藏在场景里、章末留半步”的平台节奏

## 10. 起点编辑攻略已经内置了哪些东西

我已经把 `C:\workspace_2\xiaoshuo_skills\起点网站编辑攻略` 里真正会影响写作的部分，提炼进 skill 里了。

重点吸收了这些规则：

- 历史文读者更看重逻辑、情怀、时代氛围，不吃无脑降智
- 主角要有压力位置、生活位置、现实问题，不能悬空
- 剧情靠冲突推动，不靠大段解释推动
- 开局和卷首要尽快亮卖点，尽快出事件
- 大纲要前详后略，越靠近当前章节越要细
- 文字要求以流畅、直白、顺口为先，不堆辞藻
- 历史文避免明显现代网络词、玩梗式对白
- 人物要有强标签、反差点和生活关系

这些规则现在主要体现在：

- `references/qidian-editor-rules.md`
- `references/qidian-opening-patterns.md`
- 两个 skill 的 `SKILL.md`

没有直接塞进 skill 的内容：

- 书名包装
- 简介文案
- 发书运营
- 评论互动

这些也重要，但不属于“写章纲 / 写正文”的核心流程。如果你后面要，我可以再给你补一个专门的“书名简介包装 skill”。

## 11. 安装位置

这两个 skill 现在除了项目目录内的源码版本，也应该同步安装到你实际调用的目录：

- `~/.codex/skills/novel-chapter-writer`
- `~/.codex/skills/novel-outline-planner`

如果后面你继续改项目里的 skill，最好也顺手同步安装版，避免“项目里是新规则，实际调用还是旧规则”。

## 12. 现在新增了专项模块层

当前这套小说 skills 已经不再只是：

- 一个写章纲的 skill
- 一个写正文的 skill

现在中间多了一层共享专项模块，放在：

`skills/novel-chapter-writer/references/modules/`

这层不是让你单独调用一个新 skill，而是让两个主 skill 在内部更像“先诊断，再生成，再审查”。

目前内置了这些模块：

- `volume_outline`
- `plot_logic`
- `character_consistency`
- `transition`
- `dialogue`
- `chapter_ending`
- `anti_ai_voice`
- `consistency_review`

### 它们分别管什么

- `volume_outline`
  管章纲和卷级结构，防止章节只剩事件流水账。
- `plot_logic`
  管动机、触发、决策、后果、兑现这条因果链。
- `character_consistency`
  管人物目标、情绪、关系、身体、声音五类连续性。
- `transition`
  管时间、空间、情绪、视角和章末到下章第一拍的承接。
- `dialogue`
  管对白里的身份差、利益差、压迫感和刀口。
- `chapter_ending`
  管章末落点、余力和追读拉力。
- `anti_ai_voice`
  管空泛总结、套话氛围、统一腔调和过于工整的句式。
- `consistency_review`
  管完稿后的统一六检，是最后一道质量闸门。

### 现在的默认内部流程

#### 章纲阶段

`novel-outline-planner` 现在会默认结合：

- `volume_outline`
- `plot_logic`
- `chapter_ending`

如果当前章承接紧或人物复杂，还会额外参考：

- `transition`
- `character_consistency`

#### 正文阶段

`novel-chapter-writer` 现在默认不是直接硬写，而是按这个顺序内部工作：

1. 先过 `plot_logic`
2. 再过 `character_consistency`
3. 承接紧时过 `transition`
4. 关系戏和冲突戏过 `dialogue`
5. 收尾前过 `chapter_ending`
6. 文面层再过 `anti_ai_voice`
7. 完稿后强制过 `consistency_review`

### 正文现在的六检闭环

写完一章后，默认至少内部检查这六项：

1. 剧情逻辑
2. 人物目标
3. 情绪关系
4. 身体信息
5. 场景转场
6. 章末承接

任意两项不稳，就不该直接落盘，而是回对应模块修。

### 这层和原来的区别

原来更像：

- 读资料
- 写章纲或正文
- 做一轮总表自检

现在更像：

- 读资料
- 判断问题先卡在结构、人物、转场、对白还是章末
- 用对应模块补最关键的一层
- 再写章纲或正文
- 写完后统一过六检

这样做的好处是：

- 逻辑问题不再靠润色硬遮
- 人物连续性更容易守住
- 章末和下一章第一拍更容易接牢
- 去模板腔不再只靠最后临时改词

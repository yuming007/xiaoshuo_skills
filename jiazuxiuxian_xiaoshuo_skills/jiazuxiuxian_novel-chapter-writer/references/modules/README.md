# 小说专项模块索引

这些模块不是新的主 skill，而是给现有 `novel-outline-planner` 和 `novel-chapter-writer` 提供一层更可执行的诊断、修复和审查规则。

当前项目已经有：

- 小说工程
- 已写正文
- 章节总纲
- 当前剧情状态
- 人物档案

这些模块负责补足另一层能力：

- 章节因果怎么查
- 人物状态怎么续
- 转场怎么接
- 对白怎么压
- 章末怎么留半步
- 文面怎么去模板腔
- 完稿后怎么统一复查

## 默认模块链路

### 章纲阶段

默认优先级：

1. `volume_outline`
2. `plot_logic`
3. `chapter_ending`
4. `transition`
5. `character_consistency`

### 正文阶段

开写前优先级：

1. `plot_logic`
2. `character_consistency`
3. `transition`
4. `dialogue`
5. `chapter_ending`
6. `anti_ai_voice`

完稿后强制：

7. `consistency_review`

## 各模块职责

- `volume_outline`
  处理章纲和卷级结构，不让章节只剩事件流水账。
- `plot_logic`
  处理动机、触发、决策、后果、兑现这条因果链。
- `character_consistency`
  处理目标、情绪、关系、身体、声音五类人物连续性。
- `transition`
  处理时间、空间、情绪、视角和章末到下章第一拍的承接。
- `dialogue`
  处理对白里的身份差、利益差、压迫感和信息投放。
- `chapter_ending`
  处理章末落点、余力、追读拉力和下章入口。
- `anti_ai_voice`
  处理空泛总结、套话气氛、统一腔调和平均句式。
- `consistency_review`
  处理完稿后的六检闭环，是当前项目的最后一道质量闸门。

## 使用原则

- 模块不是拿来替代正文或章纲的，而是决定章纲和正文该怎么修、怎么查。
- 如果问题已经明显集中在某一层，优先调用对应模块，不要只做泛建议。
- 如果一个问题跨多个模块，先修更底层问题，再修更表层问题。
- 任何“去 AI 味”问题，都不能先于因果、人物、转场问题处理。

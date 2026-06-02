这是两个小说 skill 默认共用的小说工程目录。

你现在已经把前六章正文放进了这里，所以后续默认不需要再配置路径。

目录约定如下：

- chapters/
  存放每章正文，文件名统一为 chapter-0001.txt 这类格式
- outlines/
  存放章节大纲，默认使用 chapter-outlines.md 这一份总表
- tracking/
  存放连载追踪文件：
  - foreshadows.md
  - timeline.md
  - character-status.md

当前默认用法：

- 生成第 N 章大纲：直接调用 `novel-outline-planner`
- 生成第 N 章正文：直接调用 `novel-chapter-writer`

两个 skill 默认都会读写这个目录。

从现在开始，默认工作流是：

- 先写或修正文 / 大纲
- 再同步 tracking 文件中的伏笔、时间线、角色状态
- 然后下一次续写时优先读取 tracking，而不是每次从头翻全部正文

只有当你以后想切换到别的小说工程时，才需要额外告诉 skill 新目录位置。

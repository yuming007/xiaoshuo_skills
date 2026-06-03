# 命名规则

## 工具

- 本 skill 默认可使用本地安装的 `random_chinese_fantasy_names`
- 共享脚本位置：
  - `../../scripts/fantasy_naming.js`
  - `../../scripts/fantasy_naming_project.js`
- 默认优先使用项目过滤版：
  - `../../scripts/fantasy_naming_project.js`
- 原始版仅在你需要放大候选池时再用
- 常用调用方式：

```bash
node ../../scripts/fantasy_naming_project.js --type name --count 20 --family 陆
node ../../scripts/fantasy_naming_project.js --type clan --count 20 --kind 社
node ../../scripts/fantasy_naming_project.js --type location --count 20 --kind 河
node ../../scripts/fantasy_naming_project.js --type skill --count 20 --kind 诀
```

## 何时使用

- 需要新增角色名时
- 需要新增家族、宗门、商盟、匠户社、坊市、山岭、河川名时
- 需要新增功法、术法、法号、秘籍名时

不要为了“显得仙侠”而把已有稳定名字全部替换掉。工具主要用于：

- 新增命名
- 候选生成
- 避免你临场硬编出一堆重复味的词

## 使用原则

- 先生成一批候选，再人工筛
- 不直接无脑采用第一批输出
- 建议一次至少生成 15 到 30 个，再筛到 3 到 8 个
- 筛选标准优先级：
  - 是否符合角色/势力气质
  - 是否与现有已命名对象撞音、撞形、撞感
  - 是否好记、顺口、适合连载读者快速识别
  - 是否避免明显套用头部作品常见既视感

## 本包的实际使用提醒

- 这个包的优势是量大、覆盖广、能快速打破你临时取名的重复习惯
- 它的短板也很明显：
  - 有些名字太随机
  - 有些词组虽然仙侠，但不够稳
  - 部分功法名会过长、过花或不够贴合本书
- 所以默认工作方式应是：
  - 项目过滤脚本先做一轮筛
  - 你做筛选
  - 必要时再二次手改
- 在本项目里，适配度从高到低大致是：
  - 势力名
  - 地名
  - 功法名
  - 次要角色名
  - 核心长期角色名
- 核心长期角色名默认仍以人工定稿优先

## 本项目的筛选约束

### 人名

- 陆氏族人：
  - 默认姓 `陆`
  - 同辈可适度统一字感，但不要刻意全员同辈字模板
- 主角线近身角色：
  - 名字要稳、清、好记
  - 避免过花、过妖、过玄虚
- 反派或灰色人物：
  - 可以稍带棱角，但不要一眼就像坏人名
- 尽量避免：
  - 生僻到影响阅读
  - 三字全虚词、全玄词
  - 与已有人物过近，例如“陆清禾/陆清和”“陆青岩/陆青言”
  - 明显失真或气质错位，例如太萌、太艳、太轻佻的字

### 势力名

- 本书偏“地面经营型仙侠”，势力名不要全是高飘大词
- 优先选择：
  - 带地方感
  - 带行业感
  - 带功能感
- 例如：
  - 宗门执行机构
  - 商盟
  - 匠户社
  - 巡矿会
  - 地方家族
- 少用：
  - 过满的神魔词
  - 一看就像终极大派的名字
  - 容易和成熟作品撞风格的名字

### 地名

- 前期地图要实用，不要全是缥缈大词
- 青岚域、临河坊、青石坊市、黑石岭这一类名字方向是对的：
  - 有地貌感
  - 有功能感
  - 方便读者记忆

### 功法 / 术法 / 秘籍

- 与修炼体系一致：
  - 偏道教内丹、符箓、御气、阵脉、导引
- 少用：
  - 纯玄幻魔改爆炸词
  - 过长过花的招式名
- 前期常用名应更朴实实用：
  - 导引术
  - 养脉诀
  - 稳泉法
  - 理气篇
- 如果工具产出过长，可优先做二次裁切：
  - 保留主意象
  - 保留功能词
  - 删除堆砌修饰

## 本书推荐调用方式

### 陆氏族人候选

```bash
node ../../scripts/fantasy_naming_project.js --type name --count 30 --family 陆
```

### 本地势力候选

```bash
node ../../scripts/fantasy_naming_project.js --type clan --count 30 --kind 社
node ../../scripts/fantasy_naming_project.js --type clan --count 30 --kind 院
node ../../scripts/fantasy_naming_project.js --type clan --count 30 --kind 会
```

### 山岭水路地名候选

```bash
node ../../scripts/fantasy_naming_project.js --type location --count 30 --kind 岭
node ../../scripts/fantasy_naming_project.js --type location --count 30 --kind 河
node ../../scripts/fantasy_naming_project.js --type location --count 30 --kind 坊
```

### 前期功法候选

```bash
node ../../scripts/fantasy_naming_project.js --type skill --count 30 --kind 诀
node ../../scripts/fantasy_naming_project.js --type skill --count 30 --kind 术
```

## 使用后的处理

- 最终采用的名字，必须写回对应文件：
  - `设定/角色/*.md`
  - `设定/势力/*.md`
  - `设定/世界观/*.md`
  - `追踪/*.md`
- 如果某个名字被否决，不要在后文反复重新抽到再用

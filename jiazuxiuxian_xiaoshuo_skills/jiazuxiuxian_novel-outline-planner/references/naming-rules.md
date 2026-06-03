# 命名规则

本 skill 与 `jiazuxiuxian_novel-chapter-writer` 共用命名生成脚本：

- `../../scripts/fantasy_naming.js`
- `../../scripts/fantasy_naming_project.js`

默认优先使用项目过滤版：

- `../../scripts/fantasy_naming_project.js`

常用调用方式：

```bash
node ../../scripts/fantasy_naming_project.js --type name --count 20 --family 陆
node ../../scripts/fantasy_naming_project.js --type clan --count 20 --kind 社
node ../../scripts/fantasy_naming_project.js --type location --count 20 --kind 岭
node ../../scripts/fantasy_naming_project.js --type skill --count 20 --kind 诀
```

## 用途

- 给新增角色、势力、地名、功法先生成候选
- 先批量生成，再人工筛掉不适合本书的

## 本书筛选方向

- 偏地面经营型仙侠
- 名字要顺口、易记、能区分
- 势力名不要全是大而空的终极词
- 地名优先地貌感、路径感、资源感
- 不要直接采用第一轮抽样结果，默认先批量出候选再筛

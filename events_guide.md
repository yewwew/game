# 事件编辑指南

## 📁 文件结构
- `game.py` - 主游戏文件
- `events.json` - 事件库文件（可编辑）

## 🎮 如何编辑事件

### 1. 打开 events.json 文件
使用任何文本编辑器或代码编辑器打开 `events.json` 文件。

### 2. 事件结构（支持扩展元数据，向后兼容）
每个事件包含以下部分（加粗为新增可选字段）：
```json
{
  "事件名称": {
    "description": "事件描述文本",
    "choices": [
      {
        "text": "选项文本",
        "effects": {
          "属性名": [最小值, 最大值],
          "属性名": 固定值
        },
        "description": "选择结果描述"
      }
    ],
    "auto_roll": { },
    "tags": ["校园", "社交"],
    "weight": 3,
    "cooldown": 2,
    "once": false,
    "min_level": 1,
    "max_level": 999,
    "requires": {
      "attributes": {"智力": ">=1"},
      "flags_all": ["见过_图书馆"],
      "flags_any": []
    },
    "excludes": ["黑市"]
  }
}
```
- `weight`：出现权重，默认 1。
- `cooldown`：触发后需要至少间隔的事件次数，默认 0。
- `once`：是否只触发一次，默认 false。
- `min_level` / `max_level`：可出现的进度范围（当前以选择次数近似）。
- `requires`：前置条件，支持属性表达式（如 `">=2"`）、`flags_all` 与 `flags_any`。
- `excludes`：互斥事件名列表。

### 3. 属性类型与键名（兼容中文）
- 角色属性: `体质`, `智力`, `情商`, `幸运`
- 资源属性: `health`(生命值), `magic`(魔法值), `experience`(经验)
- 兼容中文资源键：`"生命值" -> health`, `"魔法值" -> magic`, `"经验" -> experience`

### 4. 效果格式
- 范围效果: `[最小值, 最大值]` - 随机在此范围内取值
- 固定效果: `数值` - 固定增加此数值

### 5. 添加新事件
1. 在 `events.json` 中添加新的事件对象（可选加入 `weight/cooldown/once/requires/excludes/tags`）
2. 确保格式正确（注意逗号和括号）
3. 保存文件
4. 重启游戏即可看到新事件

### 6. 修改现有事件
1. 找到要修改的事件
2. 修改 `description` 改变事件描述
3. 修改 `choices` 数组中的选项
4. 调整 `effects` 改变属性影响（支持中文键名）
5. 如需控制出现频率/节律，使用 `weight/cooldown/once`
6. 如需设置路线前置/排斥，用 `requires/excludes`
7. 保存文件并重启游戏

## 🛈 运行时行为与提示
- 系统会依据 `weight/cooldown/once/requires` 构建候选池并加权随机。
- 负面事件遵循基础概率与最小间隔规则。
- 当某事件存在 `excludes`（与其它事件互斥）时，界面会显示温和提示：
  “该选择可能限制后续路线，慎重选择”。不会透露具体互斥对象名称。

## ⚠️ 注意事项
- 确保JSON格式正确（使用在线JSON验证器检查）
- 每个事件建议提供 4 个选项
- 属性名称必须准确（区分大小写）
- 保存文件后需要重启游戏才能生效

# anki-expert

一个 Claude Code 技能插件，从文本或本地文件生成高质量 Anki 闪卡，自动导出为 `.tsv` 或 `.apkg` 格式。

## 功能

- **专家级制卡** — 遵循最小信息原则、结构化 HTML 格式、层级标签
- **多种输入源** — 内联文本、`.md`、`.txt`、`.pdf` 文件
- **自动导出** — `.tsv`（Anki 直接导入）或 `.apkg`（便携牌组文件）
- **中英文支持** — 完整的中日韩文字和混合语言支持
- **智能排版** — 成本感知的格式强调（加粗 / 斜体 / 标黄）
- **层级标签** — 多级 `::` 分隔标签，构建知识体系

## 安装

### 前置条件

导出工具 `anki-export` 需要先安装到系统 `PATH`：

```bash
pip install git+https://github.com/gong1414/anki-card-skill.git
```

### Claude Code 中安装

```
/plugin marketplace add gong1414/anki-card-skill
/plugin install anki-expert@anki-skill
```

### 验证安装

启动新的 Claude Code 会话，输入：

```
帮我做 Anki 卡片：
{
进程间通信的主要方式有共享内存和消息传递两种。
}
nidd1234567890
```

如果技能触发并生成卡片表格，说明安装成功。

## 使用方法

### 在 Claude Code 中

告诉 Claude 制作卡片：

```
帮我做 Anki 卡片：
{
衰老细胞的特征是细胞内水分减少，导致细胞萎缩，体积变小，代谢减慢。
}
nidd1726052151484
```

或从文件生成：

```
从 ./notes/lecture-5.md 生成 Anki 闪卡
```

Claude 会按照专家规则生成卡片并自动导出。

### 命令行导出工具

```bash
# 导出为 TSV（Anki 直接导入）
anki-export cards.txt -f tsv -o output.tsv

# 导出为 APKG（便携牌组文件）
anki-export cards.txt -f apkg -o output.apkg -d "我的牌组"

# 从标准输入读取
cat cards.txt | anki-export - -f tsv -o output.tsv
```

## 卡片格式

管道分隔，三个字段：

```
问题 | 答案 | 标签
------- | -------- | --------
衰老细胞的<b>根本特征</b>？ | 细胞内 <b>水分减少</b>。<br><br>nidd123 | 生物学::细胞衰老
```

### HTML 标签

| 格式 | 标签 | 成本 | 用途 |
|------|------|------|------|
| 加粗 | `<b>` | 低 | 关键词、条目名称 |
| 斜体 | `<i>` | 中 | 英文术语、缩写 |
| 标黄 | `<span style="background-color: rgb(255, 255, 0);">` | 高 | 仅最核心术语，慎用 |
| 列表 | `<ul>/<ol>` | - | 多要点答案 |
| 代码 | `<code>` | - | 代码片段 |
| 换行 | `<br>` | - | 换行 |

### 标签体系

使用 `::` 分隔的层级标签：

```
计算机科学::算法::图论::最短路径::单源最短路径
```

### nidd 编号

每张卡片答案末尾的 `nidd` + 数字用于关联原始文本来源。导出时自动从答案中剥离，移入 Anki 标签字段。

## 许可证

MIT

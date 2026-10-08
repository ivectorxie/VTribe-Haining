# KIMI_HANDOFF — 4.VTribe

> 生成时间：2026-09-29（Asia/Shanghai）。来源：Kimi Code 会话 `session_37f57596`（`~/.kimi-code/sessions/wd_4.vtribe_08a8dd0302d5/`），2026-09-27 22:16–22:37，只有这一个会话（另外两个会话已被删除）。
> 模型：前几次因 Kimi 5 小时额度用尽失败 → 改用 grok/grok-4.6 完成。

---

## 会话 — 盘点 VTRIBE 遗留工作、清理过时任务、归档人事和产品文件

### 目标
查找与 VTRIBE（微程部落）相关的 handoff、其他 provider 的 API、其他 AI agent 留下的工作项目；然后按用户指示清理和归档。

### 盘点结论（22:19）
- 仓库里**没有**明文 API Key 或 provider 配置。
- 已有的交接：`4.8 Business Plan/OKComputer_稻草人模式改造/`（`VTRIBE_AI筛选系统交付清单.md`、`岗位说明书交付清单.md`，以及 `_Docs/`、`_Data/`）。
- 其他 agent 的遗留：Eva 的简历流水线 `eva_run_state/`；多份 Kimi Agent 产出（融资路演、自驾线路抓取、官网设计包、网站优化提案 V3.2–3.7、Odoo ERP 需求、`vtribe.cn website source code.zip`）；Kay 数字人（`kay-digital-human-profile.md`、`kay-lora-training-guide.md`，`kay_digital_human/` 是空目录）。
- 当时 Git：master 只有 3 个 commit，eva 和 Kay 的文件还没提交。

### 用户决定（22:27）
- Eva 的 v4 登记表已由 **NOVA / CV Bank** 接手 → 清除 Eva 遗留。
- **保留**融资路演；**清除**自驾线路抓取测试、官网设计包、Website Optimization Proposal、Odoo ERP 需求 V1/V1.1、`vtribe.cn website source code.zip`。
- Kay 数字人：保留。
- Desktop / Downloads 里 VTRIBE 的人事和其他文件，按内容归档进 `4.VTribe`。

### 做了什么
1. **删除**：`eva_run_state/` 整个目录；`4.8 Business Plan/Kimi_Agent_自驾线路抓取测试.zip`；`4.7 VTribe Web/` 下的官网设计包各版本、网站优化提案 V3.2–V3.7、网站修改建议、全站文案规范表、Dev Timeline、官网源码 zip；Odoo ERP 需求 V1 / V1.1（含说明）。`4.7 VTribe Web/` 现在只剩内容生产 SOP（GEO + SEO）。
2. **人事归档**：Downloads 里和 `4.4.1` 同名同大小的 7 份通用 JD 作为重复件删除；其余移入 `4.4 HRM` 各子目录（临时目录 `4.4.3 From Desktop-Downloads` 最后已拆完删除）。
3. **按内容归位（22:37）**：

| 去向 | 内容 |
|---|---|
| `4.0 User Management/` | App 用户标签设计 |
| `4.2 Content Management/4.2.1 Content Templates/` | VTRIBE 品牌简介 |
| `4.2 Content Management/4.2.6 Product Taxonomy/`（+ `Archive/`） | 标签体系 V3.0、产品分类与标签映射 V1.1（V2.0 放进 Archive） |
| `4.7 VTribe Web/` | 入境游网站情报库 |
| `4.8 Business Plan/`（+ `Archive/`） | 旅行顾问商业模式、平台模式 V2.2、转化漏斗 V1.3、墨鱼 vs 稻草人战略启示、组织架构分阶段发展（旧版本进 Archive） |
| `4.4 HRM/4.4.1 Job Descriptions/` | 六个岗位的 JD + 绩效考核表（Q4–2027 这一套）；`人员岗位说明书/` 放具名 JD（赵杨、胡奕君、唐刚华、卢心怡、岳亚楠、戴泽荣）；`Archive/` 放历史版本和赵杨测试稿，以及较早的「破折号版」产品运营 / 市场运营 JD |
| `4.4 HRM/4.4.2 Offer Letters/` | 设计师转岗续约方案 |
| `4.4 HRM/4.4.4 招聘物料/` | 海外销售渠道专家招聘海报 |

### 当前状态
- Desktop / Downloads 里已经没有 VTRIBE 文件；SIND 的材料还留在 `Downloads/Kimi_Agent_Extracted/`（不属于 VTribe，没动）。
- Kay 数字人文件还在仓库根目录，`kay_digital_human/` 仍为空，LoRA 没训练。
- 会话里**没有**做 git commit。

### 未完成 / 可选下一步
- Kay 数字人：按 `kay-lora-training-guide.md` 落地训练数据 / LoRA，或者用 DeepSwap MCP 出素材（DeepSwap 每次调用都收费）。
- 融资路演（`4.8 Business Plan/Kimi_Agent_VTRIBE融资路演/`、`VTRIBE® China by Road 融资路演B.pptx`）已保留，会话里没有继续推进。
- 视需要把这次的删除 / 归档提交到 git。

### 怎么接着做（可直接粘贴）
> 项目在 C:\Users\vecto\Documents\4.VTribe（VTRIBE / 微程部落，入境自驾游）。上一轮已经清掉了过时任务（Eva、官网设计包、Odoo、自驾线路抓取），并把人事、产品文件归档到 4.0 / 4.2 / 4.4 / 4.7 / 4.8。请先只读看一下目录结构和 git status，确认归档结果，然后告诉我：①要不要提交这次整理；②Kay 数字人（kay-digital-human-profile.md、kay-lora-training-guide.md）下一步怎么落地。先别删任何文件。

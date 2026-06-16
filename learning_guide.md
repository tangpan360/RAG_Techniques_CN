## RAG_Techniques 学习指导（中文｜按仓库路径一步步学）

这份指南的原则是：**先按仓库既有文档与文件结构走**，只写“看哪些文件、按什么顺序学、每一步产出什么”；涉及依赖安装/具体运行命令等“操作细节”，一律以对应 notebook/脚本文件内容为准，需要时再展开。

---

### 你将获得什么

- **一套可复用的 RAG 最小模板**：文档 → 切分 → 向量索引 → 检索 → 生成 →（可选）引用证据
- **一套调优方法论**：chunk / query enhancement / retrieval / rerank / context compression 的对照实验框架
- **一套评估闭环**：有问题集 + 指标 + 回归对比，知道“到底变好没”
- **从基础到高级架构的地图**：Hierarchical / RAPTOR / GraphRAG / Self-RAG / CRAG 等

---

### 仓库结构速览（你要重点看的部分）

```text
references/RAG_Techniques
├── all_rag_techniques/                   # 教学 notebooks（核心学习材料）
├── all_rag_techniques_runnable_scripts/  # 脚本版（方便你改参数做实验）
├── helper_functions.py                   # 公共工具：加载/切分/索引/检索/回答/重试等
├── evaluation/                           # 评估相关 notebooks/脚本
├── data/                                 # 示例数据（PDF/TXT/CSV/JSON）
└── images/                               # 配图（用于理解 technique）
```

---

### 学习前的“仓库事实”（先读这些文件）

- **总目录与技术清单**：`README.md`  
  - 这是这份仓库的“官方目录索引”。我们的学习路径默认以这里的 technique 清单为主线。
- **公共代码入口**：`helper_functions.py`  
  - 多数脚本/notebook 会复用其中的“加载/切分/索引/检索/回答/重试”等函数；先认识它能更快读懂后续文件。
- **评估入口**：`evaluation/` 目录  
  - 这部分决定你是否能形成“做了 technique → 知道是否真的变好”的闭环。
- **可运行脚本入口**：`all_rag_techniques_runnable_scripts/`  
  - 这是做对照实验/改参数最快的入口（比 notebook 更适合频繁重复跑）。
- **导入/依赖健康检查**：`tests/` 目录（特别是 `tests/test_imports.py`）  
  - 它展示了仓库作者用什么方式验证 notebooks/scripts 的 imports（也间接告诉你“通常需要哪些依赖”）。

> 关于依赖/Key：本仓库多个文件会 `load_dotenv()` 并使用 `OpenAIEmbeddings`/`ChatOpenAI`。具体需要哪些环境变量、怎么运行，以你正在学习的那个 `.ipynb`/`.py` 文件顶部说明为准。

---

### 学习路线（两种都“按文件走”，任选其一）

#### 路线 1：按 `README.md` 的 technique 表顺序学习（最贴近作者组织方式）

每个条目你都按固定“三连文件路径”推进：

- **先读（why + intuition）**：`all_rag_techniques/<technique>.ipynb`
- **再跑（便于改参数复现）**：`all_rag_techniques_runnable_scripts/<technique>.py`（如果存在）
- **最后补（图与评估）**：
  - 图：`images/<technique>*.svg|png`（如果 notebook 引用）
  - 评估：`evaluation/` 下与该主题相关的 notebook/脚本（如果该 technique 有评估章节/引用）

这条路线的优点是：**不容易漏掉仓库作者认为重要的内容**；缺点是：相邻条目可能跨主题跳跃，你需要用“学习记录模板”把知识串起来。

#### 路线 2：按仓库目录模块学习（更工程化，适合建立自己的 pipeline）

按目录逐层建立能力：

- **模块 A 基础闭环**：`all_rag_techniques/simple_rag*.ipynb` → `all_rag_techniques_runnable_scripts/simple_rag.py`
- **模块 B 切分与上下文**：`choose_chunk_size.ipynb`、`semantic_chunking.ipynb`、`contextual_*`、`context_enrichment_*`
- **模块 C 查询增强**：`query_transformations.ipynb`、`HyDe_*.ipynb`、`HyPE_*.ipynb`
- **模块 D 检索后处理**：`reranking*.ipynb`、`fusion_retrieval*.ipynb`、`relevant_segment_extraction.ipynb`
- **模块 E 架构升级**：`hierarchical_indices.ipynb`、`raptor.ipynb`、`graph_rag*.ipynb`、`Microsoft_GraphRag.ipynb`
- **模块 F 可靠性/自适应**：`reliable_rag.ipynb`、`adaptive_retrieval.ipynb`、`self_rag.ipynb`、`crag.ipynb`
- **模块 G 评估贯穿**：`evaluation/` 目录（从你完成模块 B 起就要开始接入）

这条路线的优点是：更像“搭积木做系统”；缺点是：你可能需要回到 `README.md` 查漏补缺。

---

### 每次学习的统一“执行脚手架”（不依赖具体 technique）

无论你学哪个文件，都按同一套路：

- **读**：打开对应 `all_rag_techniques/<technique>.ipynb`，只先看标题/overview/图/关键流程图
- **定位代码入口**：
  - notebook 里最先出现的“核心 pipeline cell”
  - 或脚本版 `all_rag_techniques_runnable_scripts/<technique>.py` 的 `main()`/类入口
- **追溯共用实现**：在 `helper_functions.py` 里找到它调用的函数（例如 encode/检索/回答）
- **做一个最小对照实验**：只改一个变量（例如 `k`、chunk size、rerank top_n 等）
- **记录结论**：按后面的模板写“适用场景/失败模式/成本”
- **（尽早）接评估**：当你已经有一组稳定的问题集，就把它接到 `evaluation/` 的框架里做回归对比

每个阶段都遵循同一套节奏：

- **读**：先看 notebook 的“Overview/Why”
- **跑**：跑通脚本版（便于调参数）
- **改**：做最小对照实验（只改一个变量）
- **记**：写结论到你的学习笔记（模板见后文）
- **测**：尽早把评估接入（第二阶段就开始）

---

### 推荐的“起步顺序”（仅给路径，不替代文件内说明）

按下面列表顺序推进，每一步都遵循上面的“执行脚手架”：

- **Step 0（目录索引）**：`README.md`（只做一件事：选定你要学的 technique 顺序）
- **Step 1（最小闭环）**：`all_rag_techniques/simple_rag.ipynb`  
  - 对照：`all_rag_techniques_runnable_scripts/simple_rag.py`
- **Step 2（切分基础）**：`all_rag_techniques/choose_chunk_size.ipynb`  
  - 对照：`all_rag_techniques_runnable_scripts/choose_chunk_size.py`
- **Step 3（切分进阶）**：`all_rag_techniques/semantic_chunking.ipynb`  
  - 对照：`all_rag_techniques_runnable_scripts/semantic_chunking.py`
- **Step 4（查询增强）**：`all_rag_techniques/query_transformations.ipynb`  
  - 对照：`all_rag_techniques_runnable_scripts/query_transformations.py`
- **Step 5（重排）**：`all_rag_techniques/reranking.ipynb`  
  - 对照：`all_rag_techniques_runnable_scripts/reranking.py`
- **Step 6（压缩/降噪）**：`all_rag_techniques/contextual_compression.ipynb`  
  - 对照：`all_rag_techniques_runnable_scripts/contextual_compression.py`
- **Step 7（评估入口）**：`evaluation/evaluation_deep_eval.ipynb` + `evaluation/end-2-end_rag_evaluation.ipynb`

---

### 评估闭环（路径约束）

从你做完 `simple_rag` + 任意一个“改进 technique”开始，就要求你必须进入 `evaluation/` 目录选一个评估路径，把对照结果记录下来。建议你优先从：

- `evaluation/evaluation_deep_eval.ipynb`
- `evaluation/end-2-end_rag_evaluation.ipynb`

#### 你需要准备的最小评测集（强烈建议）

- **问题集**：20～50 个真实问题（来自你的目标场景）
- **参考答案要点**：每题 3～7 条要点即可
- **证据要求**（可选但很有价值）：每题标出 1～3 段“必须引用的证据”

---

### 运行与依赖（只给“定位方法”，不替代文件内说明）

如果你遇到“怎么运行/缺什么依赖”的问题，优先按下面路径定位答案：

- **先看你正在学的文件顶部**：`all_rag_techniques/*.ipynb` 的前几格 / `all_rag_techniques_runnable_scripts/*.py` 的 import 与 `parse_args()`/`main()`  
- **再看共用工具**：`helper_functions.py`（它引入的库往往是关键依赖）
- **最后看测试**：`tests/test_imports.py`（它用“执行 import 行”的方式暴露常见依赖缺失）

---

### 学习记录模板（每个 technique 一页，强制填写）

复制下面模板到你的笔记（或你自己的 `notes/` 目录）：

```text
Technique:
对应文件（notebook/脚本）:

1) 解决什么问题（Why）:
2) 核心改动点（What changes）:
3) 成本与代价（Latency/Token/复杂度/依赖）:
4) 适用场景（When to use）:
5) 不适用/失败模式（When it fails）:

实验设置：
- 数据:
- 问题集:
- 指标/观测点:

对照实验结果（只改一个变量）：
- baseline:
- variant:
- 结论:

下一步行动：
- 要不要进入“默认方案”:
- 要不要加入评测回归:
```

---

### 我们后续按这份文档怎么学（协作规则）

- **每次学习只推进一个 technique（或一个小主题）**，并且必须产出：
  - 一次可复现的运行结果（脚本/笔记本）
  - 一张对照实验表（至少 2 个设置）
  - 一段结论（是否值得进入你的默认 pipeline）
- **当你卡住**（依赖/Key/报错/效果不稳定）：
  - 我会优先用“最小改动”把你带回可跑状态
  - 然后把问题归类：环境问题 / 数据问题 / 设计问题 / 参数问题 / 评估问题

---

### 附：推荐的“默认学习顺序”（你可以直接照抄打勾）

- [ ] A1 跑通 `simple_rag`（notebook + 脚本）
- [ ] A2 做 chunk/k 的最小对照实验（记录结论）
- [ ] B1 `choose_chunk_size`
- [ ] B2 `semantic_chunking`
- [ ] C1 `query_transformations`
- [ ] D1 `reranking`
- [ ] D2 `contextual_compression`
- [ ] D3 `fusion_retrieval`
- [ ] E1 `hierarchical_indices`
- [ ] E2 `raptor`
- [ ] F1 `reliable_rag`
- [ ] F2 `self_rag`
- [ ] F3 `crag`
- [ ] Eval 建立你的 20～50 题小评测集，并形成回归流程



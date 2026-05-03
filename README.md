# Voyage AI Plugin for Dify

A **Tool-type** Dify plugin that lets Chatflow, Workflow, and Agent applications generate **vector embeddings** and **rerank documents** using [Voyage AI](https://www.mongodb.com/docs/atlas/voyageai/) models hosted on MongoDB Atlas.

> **Companion plugin:** Use the **[MongoDB Atlas Tool](https://github.com/Pash10g/dify-plugins/tree/main/mongodb/mongodb_atlas_tool)** plugin to perform vector search with the embeddings generated here. The Embed Text output can be piped directly into the Vector Search tool's **Query Vector** field.

---

## Tools

| Tool | Description |
|---|---|
| **Embed Text** | Generate a vector embedding for a single text string |
| **Rerank Documents** | Rerank a list of document strings against a query by relevance score |

---

## Typical Workflow

```
[User query]
     │
     ▼
Embed Text (input_type=query)
     │  output: text → JSON float array
     ▼
MongoDB Atlas Vector Search (query_vector = {{embed.text}})
     │  output: documents
     ▼
Rerank Documents (query, documents)
     │  output: results sorted by relevance_score
     ▼
[LLM / answer node]
```

---

## Prerequisites

- A MongoDB Atlas account with the **Voyage AI** preview feature enabled
- A [Model API key](https://www.mongodb.com/docs/atlas/voyageai/management/api-keys/) from Atlas → AI Models (key starts with `pa-`)

---

## Installation

### From Dify Marketplace
Search for **Voyage AI** in the Dify Plugin Marketplace and click **Install**.

### Local / Debug Install
```bash
cp .env.example .env
# Fill in REMOTE_INSTALL_URL and REMOTE_INSTALL_KEY from Dify Plugin Management page
pip install -r requirements.txt
python -m main
```

### Package for distribution
```bash
dify plugin package ./voyage_ai
```

---

## Configuration

When installing the plugin, you will be prompted for:

| Credential | Required | Description |
|---|---|---|
| **Voyage AI API Key** | ✅ | Atlas model API key starting with `pa-` |

To create a key: Atlas UI → your project → **AI Models** → **Create model API key**.

---

## Tool Reference

### Embed Text

Generate a vector embedding for a single text. Returns the embedding as a JSON float array string, ready to pipe into the **MongoDB Atlas Vector Search** tool.

| Parameter | Type | Required | Form | Description |
|---|---|---|---|---|
| `text` | string | ✅ | llm | The text to embed. Pipe a workflow variable directly here (e.g. `{{sys.query}}`) |
| `model` | select | ❌ | form | Embedding model (default `voyage-4`) |
| `input_type` | select | ❌ | form | `query` (for search), `document` (for indexing), or empty for generic (default `query`) |
| `output_dimensions` | select | ❌ | form | Output dimensions: 256, 512, 1024, or 2048 (model default if blank) |
| `truncation` | boolean | ❌ | form | Truncate texts exceeding model token limit (default true) |

**Output (JSON message):**
```json
{
  "model": "voyage-4",
  "input_type": "query",
  "dimensions": 1024,
  "total_tokens": 6,
  "embedding": [0.01, -0.03, ...],
  "embedding_json": "[0.01, -0.03, ...]"
}
```

**Output (text message):** The embedding as a plain JSON array string — pipe `{{embed_text.text}}` directly into Vector Search's `query_vector` field.

---

### Rerank Documents

Rerank a list of documents against a query. Returns documents sorted by relevance score (highest first).

| Parameter | Type | Required | Form | Description |
|---|---|---|---|---|
| `query` | string | ✅ | llm | The search query |
| `documents` | string | ✅ | llm | JSON array of document strings, e.g. `["doc one", "doc two"]` |
| `model` | select | ❌ | form | Reranking model (default `rerank-2.5`) |
| `top_k` | number | ❌ | llm | Return only top K results (blank = return all) |
| `truncation` | boolean | ❌ | form | Truncate long documents (default true) |

**Output:**
```json
{
  "model": "rerank-2.5",
  "query": "company goals",
  "count": 3,
  "total_tokens": 120,
  "results": [
    {"index": 0, "relevance_score": 0.847, "document": "This quarter..."},
    {"index": 2, "relevance_score": 0.269, "document": "Photosynthesis..."},
    {"index": 1, "relevance_score": 0.249, "document": "20th-century..."}
  ]
}
```

---

## Supported Models

### Embedding Models

| Model | Dimensions | Context | Description |
|---|---|---|---|
| `voyage-4-large` | 1024 (default), 256, 512, 2048 | 32K | Best quality, multilingual |
| `voyage-4` | 1024 (default), 256, 512, 2048 | 32K | Balanced quality/cost (**recommended**) |
| `voyage-4-lite` | 1024 (default), 256, 512, 2048 | 32K | Lowest latency and cost |
| `voyage-4-nano` | 512 (default), 128, 256 | 32K | Open-weight model |
| `voyage-context-3` | 1024 (default), 256, 512, 2048 | 32K | Contextualized chunk embeddings |
| `voyage-code-3` | 1024 (default), 256, 512, 2048 | 32K | Code and technical documentation |
| `voyage-finance-2` | 1024 (fixed) | 32K | Finance RAG |
| `voyage-law-2` | 1024 (fixed) | 16K | Legal RAG |
| `voyage-3-large` | 1024 (default), 256, 512, 2048 | 32K | Previous generation general |
| `voyage-3.5` | 1024 (default), 256, 512, 2048 | 32K | Previous generation general |
| `voyage-3.5-lite` | 1024 (default), 256, 512, 2048 | 32K | Previous generation lite |
| `voyage-code-2` | 1536 (fixed) | 16K | Previous generation code |

### Reranking Models

| Model | Context | Description |
|---|---|---|
| `rerank-2.5` | 32K | Highest accuracy (**recommended**, 200M free tokens) |
| `rerank-2.5-lite` | 32K | Fast and cost-effective (200M free tokens) |
| `rerank-2` | 16K | Previous generation, multilingual |
| `rerank-2-lite` | 8K | Previous generation lite, multilingual |

---

## Support

- **GitHub Issues:** https://github.com/mongodb-developer/dify-plugins-mongodbatlas-tool/issues
- **MongoDB Developer Community:** https://www.mongodb.com/community/forums/

---

## License

Apache 2.0 — see [LICENSE](LICENSE) for details.

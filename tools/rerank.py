import json
import logging
from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

logger = logging.getLogger(__name__)


class RerankTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        import voyageai

        api_key = self.runtime.credentials.get("voyage_api_key", "").strip()
        if not api_key:
            raise ValueError("Voyage AI API key is missing from provider credentials.")

        query = (tool_parameters.get("query") or "").strip()
        if not query:
            raise ValueError("query is required.")

        documents_param = tool_parameters.get("documents")
        if not documents_param:
            raise ValueError("documents is required.")

        # Accept: native list (piped from another tool), or JSON string
        if isinstance(documents_param, list):
            documents = documents_param
        elif isinstance(documents_param, str) and documents_param.strip():
            try:
                documents = json.loads(documents_param.strip())
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid documents JSON: {e}")
        else:
            raise ValueError("documents must be a non-empty JSON array of strings.")

        if not isinstance(documents, list) or not documents:
            raise ValueError("documents must be a non-empty JSON array of strings.")

        # Ensure each element is a string (convert dicts to JSON strings if needed)
        documents = [
            json.dumps(d, ensure_ascii=False) if isinstance(d, dict) else str(d)
            for d in documents
        ]

        model = (tool_parameters.get("model") or "rerank-2.5").strip()
        top_k_raw = tool_parameters.get("top_k")
        top_k = int(top_k_raw) if top_k_raw is not None and str(top_k_raw).strip() != "" else None
        truncation = bool(tool_parameters.get("truncation") if tool_parameters.get("truncation") is not None else True)

        logger.info(
            "[voyage_ai][rerank] model='%s' docs=%d top_k=%s truncation=%s query='%s'",
            model, len(documents), top_k, truncation, query[:80],
        )

        client = voyageai.Client(api_key=api_key)
        result = client.rerank(
            query,
            documents,
            model=model,
            top_k=top_k,
            truncation=truncation,
        )

        ranked = [
            {
                "index": r.index,
                "relevance_score": r.relevance_score,
                "document": r.document,
            }
            for r in result.results
        ]

        logger.info(
            "[voyage_ai][rerank] returned %d results total_tokens=%s",
            len(ranked),
            getattr(result, "total_tokens", "n/a"),
        )

        for r in ranked:
            yield self.create_json_message(r)

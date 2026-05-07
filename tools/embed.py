import json
import logging
from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

logger = logging.getLogger(__name__)

# Models that do NOT support output_dimensions (fixed dimension)
_FIXED_DIMENSION_MODELS = {"voyage-finance-2", "voyage-law-2", "voyage-code-2", "voyage-multimodal-3"}


class EmbedTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        import voyageai

        api_key = self.runtime.credentials.get("voyage_api_key", "").strip()
        if not api_key:
            raise ValueError("Voyage AI API key is missing from provider credentials.")

        # Accept a single plain string — no JSON wrapping needed from the user
        text = (tool_parameters.get("text") or "").strip()
        if not text:
            raise ValueError("text is required.")

        model = (tool_parameters.get("model") or "voyage-4").strip()
        input_type_raw = (tool_parameters.get("input_type") or "").strip()
        input_type = input_type_raw if input_type_raw in ("query", "document") else None
        truncation = bool(
            tool_parameters.get("truncation")
            if tool_parameters.get("truncation") is not None
            else True
        )

        # output_dimensions — only pass if model supports it and user set a value
        output_dim_raw = str(tool_parameters.get("output_dimensions") or "").strip()
        output_dimensions = None
        if output_dim_raw and model not in _FIXED_DIMENSION_MODELS:
            try:
                output_dimensions = int(output_dim_raw)
            except ValueError:
                pass

        logger.info(
            "[voyage_ai][embed] model='%s' input_type=%s output_dimensions=%s truncation=%s text_len=%d",
            model, input_type, output_dimensions, truncation, len(text),
        )

        client = voyageai.Client(api_key=api_key)

        embed_kwargs: dict[str, Any] = dict(
            texts=[text],
            model=model,
            input_type=input_type,
            truncation=truncation,
        )
        if output_dimensions is not None:
            embed_kwargs["output_dimension"] = output_dimensions

        result = client.embed(**embed_kwargs)

        embedding: list[float] = result.embeddings[0]
        dimensions = len(embedding)
        total_tokens = getattr(result, "total_tokens", None)

        logger.info(
            "[voyage_ai][embed] generated embedding dim=%d total_tokens=%s",
            dimensions, total_tokens,
        )

        # Return the embedding as a JSON string so it can be piped directly into
        # the MongoDB Atlas Vector Search tool's `query_vector` parameter.
        embedding_json = json.dumps(embedding)

        # Yield the JSON message first so the structured output (with the native
        # `embedding` list) is available for variable piping in Dify workflows.
        # The `embedding` field is a flat list[float] that can be wired directly
        # into Vector Search's `query_vector` parameter.
        yield self.create_json_message({
            "model": model,
            "input_type": input_type,
            "dimensions": dimensions,
            "total_tokens": total_tokens,
            "embedding": embedding,
            "embedding_json": embedding_json,
        })
        yield self.create_text_message(embedding_json)

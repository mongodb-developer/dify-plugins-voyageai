from typing import Any, Mapping

from dify_plugin.interfaces.tool import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class VoyageAIProvider(ToolProvider):
    """
    Provider class for Voyage AI plugin.
    Validates the API key by generating a test embedding.
    """

    def _validate_credentials(self, credentials: Mapping[str, Any]) -> None:
        try:
            import voyageai

            api_key = credentials.get("voyage_api_key", "").strip()
            if not api_key:
                raise ToolProviderCredentialValidationError(
                    "Voyage AI API key is required."
                )

            client = voyageai.Client(api_key=api_key)
            # Lightweight validation: embed a single short string
            result = client.embed(["ping"], model="voyage-4-lite")
            if not result.embeddings or not result.embeddings[0]:
                raise ToolProviderCredentialValidationError(
                    "API key validation failed: empty embedding returned."
                )

        except ToolProviderCredentialValidationError:
            raise
        except Exception as e:
            raise ToolProviderCredentialValidationError(
                f"Failed to validate Voyage AI API key: {str(e)}"
            )

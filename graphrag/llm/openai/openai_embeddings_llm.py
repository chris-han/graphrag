# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

"""The EmbeddingsLLM class."""

import logging

import numpy as np
from typing_extensions import Unpack

from graphrag.llm.base import BaseLLM
from graphrag.llm.types import (
    EmbeddingInput,
    EmbeddingOutput,
    LLMInput,
)

from .openai_configuration import OpenAIConfiguration
from .types import OpenAIClientTypes

log = logging.getLogger(__name__)

class OpenAIEmbeddingsLLM(BaseLLM[EmbeddingInput, EmbeddingOutput]):
    """A text-embedding generator LLM."""

    _client: OpenAIClientTypes
    _configuration: OpenAIConfiguration

    def __init__(self, client: OpenAIClientTypes, configuration: OpenAIConfiguration):
        self.client = client
        self.configuration = configuration

    async def _execute_llm(
        self, input: EmbeddingInput, **kwargs: Unpack[LLMInput]
    ) -> EmbeddingOutput | None:
        args = {
            "model": self.configuration.model,
            **(kwargs.get("model_parameters") or {}),
        }
                        
        # add try catch block to handle exceptions
        try:
            log.info(f"Calling OpenAI embeddings API with args: {args}")  # noqa: G004
            # embedding = await self.client.embeddings.create(
            #     input=input,
            #     **args,
            # )
            # return [d.embedding for d in embedding.data] # type: ignore
            ret = await self.client.embeddings.create(
                input=input,
                **args,
                extra_headers={'content-type': 'application/json'},
            )
            log.info(f"Embeddings API response: {ret}")
            
            if isinstance(ret, dict) and 'data' in ret:
                return ret['data']  # Return the 'data' part of the dictionary
            else:
                log.error("Unexpected response format")
                return np.array([], dtype=float) 
                
        except Exception as e:#'str' object has no attribute 'data'
            log.exception(f"Exception while creating embeddings: {e}")  # noqa: G004, TRY401
            return np.array([], dtype=float)  # type: ignore # Return an empty 1-D array

# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

"""Parameterization settings for the default configuration."""

from pydantic import BaseModel, Field

import graphrag.config.defaults as defs
from graphrag.index.operations.chunk_text import ChunkStrategyType

class ChunkingConfig(BaseModel):
    """Configuration section for chunking."""

    size: int = Field(description="The chunk size to use.", default=defs.CHUNK_SIZE)
    overlap: int = Field(
        description="The chunk overlap to use.", default=defs.CHUNK_OVERLAP
    )
    group_by_columns: list[str] = Field(
        description="The chunk by columns to use.",
        default=defs.CHUNK_GROUP_BY_COLUMNS,
    )
    
    encoding_model: str | None = Field(
        default=None, description="The encoding model to use."
    )

    type: str | None = Field(
        default=ChunkStrategyType.delimiter, description="The chunking method to use. Values:ChunkStrategyType.delimiter|tokens|sentence Default: delimiter"
    )

    delimiter_string: str | None = Field(
        default=defs.CHUNK_DELIMITER_STRING, description="The delimiter_string to use as text.split(delimiter_string)."
    )

    strategy: dict | None = Field(
        description="The chunk strategy to use, overriding the default tokenization strategy",
        default=None,
    )


    def resolved_strategy(self, encoding_model: str | None) -> dict:
        """Get the resolved chunking strategy."""
        from graphrag.index.operations.chunk_text import ChunkStrategyType

        return self.strategy or {
            "type": self.type or ChunkStrategyType.tokens,
            "chunk_size": self.size,
            "chunk_overlap": self.overlap,
            "delimiter_string": self.delimiter_string,
            "group_by_columns": self.group_by_columns,
            "encoding_name": encoding_model or self.encoding_model,
            
        }

# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

"""A module containing chunk strategies."""

from collections.abc import Iterable
from typing import Any

import nltk
import tiktoken
from datashaper import ProgressTicker

import graphrag.config.defaults as defs
from graphrag.index.operations.chunk_text.typing import TextChunk
from graphrag.index.text_splitting.text_splitting import Tokenizer


def run_tokens(
    input: list[str], args: dict[str, Any], tick: ProgressTicker
) -> Iterable[TextChunk]:
    """Chunks text into chunks based on encoding tokens."""
    tokens_per_chunk = args.get("chunk_size", defs.CHUNK_SIZE)
    chunk_overlap = args.get("chunk_overlap", defs.CHUNK_OVERLAP)
    encoding_name = args.get("encoding_name", defs.ENCODING_MODEL)
    enc = tiktoken.get_encoding(encoding_name)

    def encode(text: str) -> list[int]:
        if not isinstance(text, str):
            text = f"{text}"
        return enc.encode(text)

    def decode(tokens: list[int]) -> str:
        return enc.decode(tokens)

    return _split_text_on_tokens(
        input,
        Tokenizer(
            chunk_overlap=chunk_overlap,
            tokens_per_chunk=tokens_per_chunk,
            encode=encode,
            decode=decode,
        ),
        tick,
    )


# Adapted from - https://github.com/langchain-ai/langchain/blob/77b359edf5df0d37ef0d539f678cf64f5557cb54/libs/langchain/langchain/text_splitter.py#L471
# So we could have better control over the chunking process
def _split_text_on_tokens(
    texts: list[str], enc: Tokenizer, tick: ProgressTicker
) -> list[TextChunk]:
    """Split incoming text and return chunks."""
    result = []
    mapped_ids = []

    for source_doc_idx, text in enumerate(texts):
        encoded = enc.encode(text)
        tick(1)
        mapped_ids.append((source_doc_idx, encoded))

    input_ids: list[tuple[int, int]] = [
        (source_doc_idx, id) for source_doc_idx, ids in mapped_ids for id in ids
    ]

    start_idx = 0
    cur_idx = min(start_idx + enc.tokens_per_chunk, len(input_ids))
    chunk_ids = input_ids[start_idx:cur_idx]
    while start_idx < len(input_ids):
        chunk_text = enc.decode([id for _, id in chunk_ids])
        doc_indices = list({doc_idx for doc_idx, _ in chunk_ids})
        result.append(
            TextChunk(
                text_chunk=chunk_text,
                source_doc_indices=doc_indices,
                n_tokens=len(chunk_ids),
            )
        )
        start_idx += enc.tokens_per_chunk - enc.chunk_overlap
        cur_idx = min(start_idx + enc.tokens_per_chunk, len(input_ids))
        chunk_ids = input_ids[start_idx:cur_idx]

    return result


def run_sentences(
    input: list[str], _args: dict[str, Any], tick: ProgressTicker
) -> Iterable[TextChunk]:
    """Chunks text into multiple parts by sentence."""
    encoding_name = _args.get("encoding_name", defs.ENCODING_MODEL)
    enc = tiktoken.get_encoding(encoding_name)
    for doc_idx, text in enumerate(input):
        sentences = nltk.sent_tokenize(text)
        sentences = [sentence for sentence in sentences if isinstance(sentence,str)]
        for sentence in sentences:
            chunk_ids = enc.encode(sentence)
            n_tokens=len(chunk_ids)
            yield TextChunk(
                text_chunk=sentence,
                source_doc_indices=[doc_idx],
                n_tokens=n_tokens,
            )
        tick(1)

def run_delimiter(
    input: list[str], _args: dict[str, Any], tick: ProgressTicker
) -> Iterable[TextChunk]:
    """Chunks text into multiple parts by sentence."""
    delimiter_string=_args.get("delimiter_string",defs.CHUNK_DELIMITER_STRING)
    encoding_name = _args.get("encoding_name", defs.ENCODING_MODEL)
    enc = tiktoken.get_encoding(encoding_name)
    for doc_idx, text in enumerate(input):
        if delimiter_string in text:
            chunks = text.split(delimiter_string)
            chunks = [chunk for chunk in chunks if isinstance(chunk,str)]
            for chunk in chunks:
                chunk_ids = enc.encode(chunk)
                n_tokens=len(chunk_ids)
                yield TextChunk(
                    text_chunk=chunk,
                    source_doc_indices=[doc_idx],
                    n_tokens=n_tokens,
                )
            tick(1)
        else:
            results = run_tokens(input,_args,tick)
            for result in results:
                yield result
            # return results # type: ignore

tokens = [
    27,
    60396,
    106130,
    54780,
    5122,
    32,
    100389,
    23671,
    87,
    91,
    82700,
    99361,
    101111,
    91,
    73345,
    29991,
    9685,
    100523,
    24342,
    99641,
    99469,
    99523,
    99488,
    100200,
    93823,
    104512,
    72448,
    99403,
    100341,
    73345,
    3407,
    27,
    60396,
    106130,
    54780,
    5122,
    32,
    100389,
    23671,
    87,
    91,
    82700,
    99361,
    101111,
    91,
    99403,
    102193,
    9685,
    118793,
    100622,
    101055,
    108097,
    110393,
    15946,
    100795,
    101121,
    31235,
    80942,
    5373,
    81800,
    100082,
    5373,
    47874,
    101924,
    106654,
    108097,
    3837,
    20412,
    101908,
    99286,
    22418,
    9370,
    115932,
    3837,
    68536,
    104512,
    99403,
    20412,
    118793,
    18493,
    47874,
    101924,
    5373,
    105262,
    101899,
    33108,
    115955,
    100178,
    101047,
    31235,
    49828,
    47534,
    33108,
    31235,
    104775,
    104069,
    104085,
    33108,
    102011,
    3837,
    99999,
    3837,
    100362,
    101137,
    99599,
    118181,
    100367,
    33108,
    70500,
    9370,
    100634,
    104512,
    99403,
    3837,
    20412,
    100341,
    100634,
    101924,
    113787,
    5373,
    107487,
    113787,
    33108,
    111899,
    9370,
    100270,
    99257,
    3837,
    101451,
    101345,
    20412,
    104236,
    99599,
    102145,
    99286,
    22418,
    26288,
    100160,
    101945,
    104539,
    8997,
    21894,
    73345,
    50511,
    118641,
    102145,
    101356,
    100200,
    109324,
    33108,
    99186,
    60726,
    99399,
    90172,
    104820,
    3837,
    23031,
    99252,
    103247,
    99488,
    3837,
    23031,
    105515,
    100545,
    17714,
    104532,
    27442,
    3837,
    100374,
    100634,
    33108,
    107022,
    105638,
    107591,
    3837,
    110960,
    99599,
    33108,
    105638,
    100138,
    101882,
    3837,
    101910,
    13343,
    16872,
    31235,
    106277,
    9370,
    952,
    33108,
    20074,
    99361,
    3837,
    32664,
    35987,
    93823,
    9370,
    100182,
    5373,
    39352,
    49567,
    102025,
    33108,
    102054,
    115746,
    9370,
    104512,
    3837,
    103983,
    33108,
    102102,
    100634,
    102938,
    105470,
    85329,
    3837,
    104004,
    104512,
    9370,
    118182,
    3837,
    103967,
    100634,
    27369,
    100142,
    3837,
    101884,
    35987,
    93823,
    85329,
    9370,
    103967,
    107415,
    33108,
    39352,
    3837,
    101884,
    35987,
    93823,
    20074,
    99814,
    9370,
    108690,
    33108,
    114919,
    3837,
    17714,
    101924,
    110166,
    100393,
    102421,
    3837,
    17714,
    104595,
    107487,
    100341,
    99570,
    3837,
    17714,
    115955,
    99553,
    102041,
    104282,
    3837,
    103941,
    17714,
    100634,
    99185,
    116430,
    8997,
    17,
    15,
    15,
    24,
    7948,
    19,
    9754,
    91111,
    106638,
    5373,
    104439,
    101888,
    102145,
    101356,
    100200,
    100878,
    9370,
    99895,
    105885,
    87243,
    101055,
    101093,
    101080,
    99403,
    116863,
    99797,
    112144,
    102756,
    100637,
    9370,
    63703,
    101965,
    99568,
    102277,
    77835,
    99630,
    3837,
    104181,
    44063,
    112144,
    104512,
    99403,
    60610,
    17714,
    104069,
    112144,
    109324,
    9370,
    109793,
    100653,
    1773,
    17,
    15,
    16,
    20,
    7948,
    3837,
    99599,
    117552,
    18493,
    26940,
    100642,
    104009,
    111857,
    112864,
    25067,
    110185,
    17447,
    100642,
    109329,
    101882,
    5122,
    67338,
    104512,
    100622,
    104085,
    18493,
    102145,
    99286,
    22418,
    5373,
    103983,
    102054,
    5373,
    104009,
    47874,
    5373,
    100641,
    100674,
    5373,
    100341,
    99570,
    5373,
    101902,
    104063,
    102159,
    104944,
    41146,
    112324,
    99602,
    104069,
    100154,
    1773,
    62926,
    101041,
    57191,
    108349,
    9370,
    104643,
    32664,
    104512,
    72448,
    104272,
    3837,
    91676,
    67338,
    104512,
    32664,
    31843,
    104009,
    108590,
    107594,
    47874,
    102054,
    3837,
    100627,
    101924,
    110166,
    101904,
    3837,
    101931,
    107487,
    101070,
    3837,
    101048,
    100182,
    99464,
    3837,
    102330,
    101046,
    105880,
    100674,
    3837,
    103983,
    85329,
    100745,
    85767,
    3837,
    101884,
    101065,
    100182,
    105176,
    33108,
    109426,
    46670,
    99781,
    1773
  ]
print(len(tokens))
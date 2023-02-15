import io
import json

import pytest
from aiohttp import ClientSession

import openai
from openai import error


pytestmark = [pytest.mark.asyncio]


# FILE TESTS
async def test_file_upload():
    result = await openaipro.File.acreate(
        file=io.StringIO(json.dumps({"text": "test file data"})),
        purpose="search",
    )
    assert result.purpose == "search"
    assert "id" in result

    result = await openaipro.File.aretrieve(id=result.id)
    assert result.status == "uploaded"


# COMPLETION TESTS
async def test_completions():
    result = await openaipro.Completion.acreate(
        prompt="This was a test", n=5, engine="ada"
    )
    assert len(result.choices) == 5


async def test_completions_multiple_prompts():
    result = await openaipro.Completion.acreate(
        prompt=["This was a test", "This was another test"], n=5, engine="ada"
    )
    assert len(result.choices) == 10


async def test_completions_model():
    result = await openaipro.Completion.acreate(prompt="This was a test", n=5, model="ada")
    assert len(result.choices) == 5
    assert result.model.startswith("ada")


async def test_timeout_raises_error():
    # A query that should take awhile to return
    with pytest.raises(error.Timeout):
        await openaipro.Completion.acreate(
            prompt="test" * 1000,
            n=10,
            model="ada",
            max_tokens=100,
            request_timeout=0.01,
        )


async def test_timeout_does_not_error():
    # A query that should be fast
    await openaipro.Completion.acreate(
        prompt="test",
        model="ada",
        request_timeout=10,
    )


async def test_completions_stream_finishes_global_session():
    async with ClientSession() as session:
        openaipro.aiosession.set(session)

        # A query that should be fast
        parts = []
        async for part in await openaipro.Completion.acreate(
            prompt="test", model="ada", request_timeout=3, stream=True
        ):
            parts.append(part)
        assert len(parts) > 1


async def test_completions_stream_finishes_local_session():
    # A query that should be fast
    parts = []
    async for part in await openaipro.Completion.acreate(
        prompt="test", model="ada", request_timeout=3, stream=True
    ):
        parts.append(part)
    assert len(parts) > 1
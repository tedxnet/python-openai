import io
import json

import pytest

import openai
from openai import error


# FILE TESTS
def test_file_upload():
    result = openaipro.File.create(
        file=io.StringIO(
            json.dumps({"prompt": "test file data", "completion": "tada"})
        ),
        purpose="fine-tune",
    )
    assert result.purpose == "fine-tune"
    assert "id" in result

    result = openaipro.File.retrieve(id=result.id)
    assert result.status == "uploaded"


# COMPLETION TESTS
def test_completions():
    result = openaipro.Completion.create(prompt="This was a test", n=5, engine="ada")
    assert len(result.choices) == 5


def test_completions_multiple_prompts():
    result = openaipro.Completion.create(
        prompt=["This was a test", "This was another test"], n=5, engine="ada"
    )
    assert len(result.choices) == 10


def test_completions_model():
    result = openaipro.Completion.create(prompt="This was a test", n=5, model="ada")
    assert len(result.choices) == 5
    assert result.model.startswith("ada")


def test_timeout_raises_error():
    # A query that should take awhile to return
    with pytest.raises(error.Timeout):
        openaipro.Completion.create(
            prompt="test" * 1000,
            n=10,
            model="ada",
            max_tokens=100,
            request_timeout=0.01,
        )


def test_timeout_does_not_error():
    # A query that should be fast
    openaipro.Completion.create(
        prompt="test",
        model="ada",
        request_timeout=10,
    )
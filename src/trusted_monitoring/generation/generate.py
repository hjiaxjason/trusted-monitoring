"""Backend-agnostic text generation for U (and, if used, the trusted editor).

Wraps either a local HF `transformers` pipeline or a hosted OpenAI-compatible
API (Together/Fireworks) behind one interface so the rest of the pipeline
never has to know which backend a given model config uses.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ModelConfig:
    name: str
    backend: str  # "hf" | "hosted"
    model_id: str
    max_new_tokens: int = 1024
    temperature: float = 0.7

    @classmethod
    def from_yaml_entry(cls, entry: dict) -> ModelConfig:
        return cls(
            name=entry["name"],
            backend=entry["backend"],
            model_id=entry["model_id"],
            max_new_tokens=entry.get("max_new_tokens", 1024),
            temperature=entry.get("temperature", 0.7),
        )


class Generator:
    """Loads a model per `ModelConfig` and exposes `generate(system, user) -> str`."""

    def __init__(self, config: ModelConfig):
        self.config = config
        self._client = None  # lazily initialized by _load()

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        if self._client is None:
            self._load()
        if self.config.backend == "hf":
            return self._generate_hf(system_prompt, user_prompt)
        if self.config.backend == "hosted":
            return self._generate_hosted(system_prompt, user_prompt)
        raise ValueError(f"Unknown backend: {self.config.backend!r}")

    def _load(self) -> None:
        raise NotImplementedError(
            "TODO: for backend='hf', load AutoModelForCausalLM + AutoTokenizer "
            "via transformers; for backend='hosted', construct an OpenAI-compatible "
            "client pointed at the Together/Fireworks base URL using the API key "
            "from the environment (see .env.example)."
        )

    def _generate_hf(self, system_prompt: str, user_prompt: str) -> str:
        raise NotImplementedError("TODO: apply chat template, generate, decode.")

    def _generate_hosted(self, system_prompt: str, user_prompt: str) -> str:
        raise NotImplementedError("TODO: call chat.completions.create with self._client.")

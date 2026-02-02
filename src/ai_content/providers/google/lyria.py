"""
Google Lyria RealTime music provider.

Uses WebSocket streaming for real-time music generation.
"""

import asyncio
import logging
from datetime import datetime, timezone
from pathlib import Path

from ai_content.core.registry import ProviderRegistry
from ai_content.core.result import GenerationResult
from ai_content.core.exceptions import (
    ProviderError,
    AuthenticationError,
    GenerationError,
)
from ai_content.config import get_settings

logger = logging.getLogger(__name__)


@ProviderRegistry.register_music("lyria")
class GoogleLyriaProvider:
    """
    Google Lyria RealTime music provider.

    Features:
        - Real-time streaming generation
        - Weighted prompt support
        - BPM and temperature control
        - Instrumental only (no vocals)

    Example:
        >>> provider = GoogleLyriaProvider()
        >>> result = await provider.generate(
        ...     "smooth jazz fusion",
        ...     bpm=95,
        ...     duration_seconds=30,
        ... )
    """

    name = "lyria"
    supports_vocals = False
    supports_realtime = True
    supports_reference_audio = False

    def __init__(self):
        self.settings = get_settings().google
        self._client = None

    def _get_client(self):
        """Lazy-load the Google GenAI client."""
        if self._client is None:
            try:
                from google import genai

                api_key = self.settings.api_key
                if not api_key:
                    raise AuthenticationError("lyria")
                # Lyria RealTime requires v1alpha API version
                # https://ai.google.dev/gemini-api/docs/music-generation
                self._client = genai.Client(
                    api_key=api_key,
                    http_options={"api_version": "v1alpha"},
                )
            except ImportError:
                raise ProviderError(
                    "lyria",
                    "google-genai package not installed. Run: pip install google-genai",
                )
        return self._client

    async def generate(
        self,
        prompt: str,
        *,
        bpm: int = 120,
        duration_seconds: int = 30,
        lyrics: str | None = None,
        reference_audio_url: str | None = None,
        output_path: str | None = None,
        temperature: float = 1.0,
    ) -> GenerationResult:
        """
        Generate music using Lyria RealTime streaming.

        Note:
            Lyria does not support vocals or lyrics. The lyrics parameter
            is ignored for compatibility with the MusicProvider protocol.
        """
        from google.genai import types

        client = self._get_client()

        logger.info(f"🎵 Lyria: Generating {duration_seconds}s at {bpm} BPM")
        logger.debug(f"   Prompt: {prompt[:50]}...")

        if lyrics:
            logger.warning("Lyria does not support vocals/lyrics. Ignoring lyrics parameter.")

        audio_chunks: list[bytes] = []

        try:
            async with client.aio.live.music.connect(model=self.settings.music_model) as session:
                # Set weighted prompts
                await session.set_weighted_prompts(
                    prompts=[types.WeightedPrompt(text=prompt, weight=1.0)]
                )

                # Configure generation
                await session.set_music_generation_config(
                    config=types.LiveMusicGenerationConfig(
                        bpm=bpm,
                        temperature=temperature,
                    )
                )

                # Start streaming
                await session.play()

                start_time = asyncio.get_event_loop().time()

                while True:
                    turn = session.receive()
                    async for response in turn:
                        # Use audio_chunks as per official docs
                        # https://ai.google.dev/gemini-api/docs/music-generation
                        if (
                            response.server_content
                            and hasattr(response.server_content, "audio_chunks")
                            and response.server_content.audio_chunks
                        ):
                            audio_chunks.append(response.server_content.audio_chunks[0].data)

                    elapsed = asyncio.get_event_loop().time() - start_time
                    if elapsed >= duration_seconds:
                        await session.pause()
                        break

        except Exception as e:
            logger.error(f"Lyria generation failed: {e}")
            return GenerationResult(
                success=False,
                provider=self.name,
                content_type="music",
                error=str(e),
            )

        if not audio_chunks:
            return GenerationResult(
                success=False,
                provider=self.name,
                content_type="music",
                error="No audio data received",
            )

        # Combine audio chunks
        audio_data = b"".join(audio_chunks)

        # Save if output path provided
        file_path = None
        if output_path:
            file_path = Path(output_path)
        else:
            output_dir = get_settings().output_dir
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            file_path = output_dir / f"lyria_{timestamp}.wav"

        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_bytes(audio_data)

        logger.info(f"✅ Lyria: Saved to {file_path}")

        return GenerationResult(
            success=True,
            provider=self.name,
            content_type="music",
            file_path=file_path,
            data=audio_data,
            duration_seconds=duration_seconds,
            metadata={
                "bpm": bpm,
                "temperature": temperature,
                "prompt": prompt,
            },
        )

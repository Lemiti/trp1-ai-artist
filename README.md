# AI Content Generator

A multi-provider AI content generation framework for music, video, and images.

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

- **Multi-Provider Architecture**: Google (Lyria, Veo, Imagen), AIMLAPI (MiniMax), KlingAI
- **Plugin System**: Add new providers without modifying core code
- **Style Presets**: Pre-configured prompts for jazz, blues, cinematic, and more
- **Async-First**: Non-blocking operations with proper async/await
- **Type-Safe**: Full type hints with Pydantic configuration
- **CLI Interface**: Easy-to-use command-line tool

## 🚀 Quick Start

### Installation

```bash
# Clone and install
git clone <repository>
cd ai-content
uv sync

# Or install as package
pip install -e .
```

### Configuration

Create `.env` file:

```env
# Google APIs (Lyria, Veo, Imagen)
GEMINI_API_KEY=your_google_api_key

# AIMLAPI (MiniMax)
AIMLAPI_KEY=your_aimlapi_key

# KlingAI Direct
KLINGAI_API_KEY=your_kling_api_key
KLINGAI_SECRET_KEY=your_kling_secret
```

### Basic Usage

```bash
# Generate music with preset
uv run ai-content music --style jazz --provider lyria

# Generate music with custom prompt
uv run ai-content music \
  --prompt "Smooth jazz fusion with walking bass" \
  --provider lyria \
  --bpm 95

# Generate video
uv run ai-content video \
  --prompt "Dragon soaring over mountains" \
  --provider veo \
  --aspect 16:9

# List available options
uv run ai-content list-providers
uv run ai-content list-presets
```

## 📦 Package Structure

```
ai-content/
├── src/ai_content/          # Main package
│   ├── core/                # Protocols, Registry, Result
│   ├── config/              # Pydantic settings
│   ├── providers/           # Provider implementations
│   │   ├── google/          # Lyria, Veo, Imagen
│   │   ├── aimlapi/         # MiniMax
│   │   └── kling/           # KlingAI Direct
│   ├── pipelines/           # Orchestration workflows
│   ├── integrations/        # External services
│   ├── presets/             # Style presets
│   ├── utils/               # Utilities
│   └── cli/                 # Typer CLI
├── configs/                 # YAML configuration
├── docs/                    # Documentation
├── examples/                # Example scripts (8)
└── .agent/                  # AI agent configuration
```

## 🎬 Full Content Pipeline

```
┌──────────────────────────────────────────────────────────────────┐
│                    FULL CONTENT PIPELINE                         │
└──────────────────────────────────────────────────────────────────┘

1️⃣ SOURCE SELECTION
   Archive.org → search_items("1930s jazz")
        │
        ▼
   ┌─────────────────┐
   │ Source metadata │
   │ • identifier    │
   │ • thumbnail_url │
   │ • audio_url     │
   └────────┬────────┘
            │
2️⃣ CONTENT GENERATION (PARALLEL)
            │
   ┌────────┴────────┐
   │                 │
   ▼                 ▼
┌──────────┐   ┌──────────┐
│ 🎵 Music │   │ 🖼️ Image │
│  Lyria   │   │  Imagen  │
│  MiniMax │   │          │
└────┬─────┘   └────┬─────┘
     │              │
     │              ▼
     │        ┌──────────┐
     │        │ 🎬 Video │
     │        │   Veo    │
     │        │   Kling  │
     │        └────┬─────┘
     │             │
3️⃣ POST-PROCESSING
     │             │
     └──────┬──────┘
            ▼
   ┌─────────────────┐
   │  Media Merge    │
   │  (FFmpeg)       │
   │  audio + video  │
   └────────┬────────┘
            │
4️⃣ OUTPUT DESTINATION
            │
            ▼
   ┌─────────────────┐
   │  Local Export   │ ← Always save locally first
   └────────┬────────┘
            │
   ┌────────┴────────┐
   │                 │
   ▼                 ▼
┌──────────┐   ┌──────────┐
│ YouTube  │   │    S3    │
│ Upload   │   │  Upload  │
└──────────┘   └──────────┘
```

## 📄 Examples

| Example | Description |
|---------|-------------|
| `01_basic_music.py` | Simplest music generation |
| `02_basic_video.py` | Simplest video generation |
| `03_lyrics_workflow.py` | Lyrics-first with structure tags |
| `04_image_to_video.py` | Animate a static image |
| `05_provider_comparison.py` | Compare multiple providers |
| `06_music_video_pipeline.py` | Full end-to-end pipeline |
| `07_archive_integration.py` | Search Archive.org for sources |
| `08_custom_provider.py` | Create your own provider |

```bash
# Run examples
python examples/01_basic_music.py jazz
python examples/06_music_video_pipeline.py cinematic space
```



## 🎵 Music Providers

| Provider | Vocals | Real-time | Reference Audio | Best For |
|----------|--------|-----------|-----------------|----------|
| **Lyria** | ❌ | ✅ | ❌ | Fast instrumentals |
| **MiniMax** | ✅ | ❌ | ✅ | Vocals, style transfer |

```python
from ai_content import ProviderRegistry
from ai_content.presets import get_music_preset

# Get preset and provider
preset = get_music_preset("jazz")
provider = ProviderRegistry.get_music("lyria")

# Generate
result = await provider.generate(
    prompt=preset.prompt,
    bpm=preset.bpm,
    duration_seconds=30,
)

if result.success:
    print(f"Saved: {result.file_path}")
```

## 🎬 Video Providers

| Provider | Speed | Quality | Image-to-Video | Best For |
|----------|-------|---------|----------------|----------|
| **Veo** | Fast (~30s) | Good | ✅ | Quick iterations |
| **Kling** | Slow (5-14min) | Highest | ✅ | Final renders |

```python
from ai_content import ProviderRegistry
from ai_content.presets import get_video_preset

# Get preset and provider
preset = get_video_preset("space")
provider = ProviderRegistry.get_video("veo")

# Generate
result = await provider.generate(
    prompt=preset.prompt,
    aspect_ratio=preset.aspect_ratio,
)
```

## 🎨 Available Presets

### Music Presets
- `jazz` - Smooth jazz fusion (95 BPM)
- `blues` - Delta blues (72 BPM)
- `ethiopian-jazz` - Ethio-jazz fusion (85 BPM)
- `cinematic` - Epic orchestral (100 BPM)
- `electronic` - Progressive house (128 BPM)
- `ambient` - Atmospheric pads (60 BPM)
- `lofi` - Lo-fi hip-hop (85 BPM)
- `rnb` - Contemporary R&B (90 BPM)

### Video Presets
- `nature` - Wildlife documentary
- `urban` - Cyberpunk cityscape
- `space` - Astronaut/sci-fi
- `abstract` - Liquid metal/geometric
- `ocean` - Underwater scenes
- `fantasy` - Dragons/epic fantasy
- `portrait` - Fashion/beauty

## 🔧 Makefile Commands

```bash
# Setup
make install              # Install dependencies

# Music Generation
make test-jazz            # Jazz preset with Lyria
make test-blues           # Blues preset
make test-ethiopian-jazz  # Ethio-Jazz preset

# Test Pipeline
make test-performance-first  # Performance-First workflow
make test-lyrics-first       # Lyrics-First workflow
make test-provider-compare   # Compare Lyria vs MiniMax

# Multi-Provider
make run-multi-music         # MiniMax Music 2.0
make run-multi-video-kling   # KlingAI v2.1

# Help
make help                 # Show all commands
```

## 🤖 AI Agent Integration

This package includes AI agent configuration for development:

- **Rules**: `.agent/rules/RULES.md` - Development standards
- **Skills**: `.agent/skills/*/SKILL.md` - Domain knowledge
- **Workflows**: `.agent/workflows/*.md` - Step-by-step guides

## 📚 Documentation

- [Architecture](docs/architecture/ARCHITECTURE.md) - System design
- [Extending Guide](docs/guides/EXTENDING.md) - Add new providers
- [Content Guidelines](docs/guides/AI_CONTENT_CREATION_GUIDELINES.md) - Best practices

## 🔌 Adding a New Provider

```python
from ai_content.core.registry import ProviderRegistry
from ai_content.core.result import GenerationResult

@ProviderRegistry.register_music("my_provider")
class MyMusicProvider:
    name = "my_provider"
    supports_vocals = True
    supports_realtime = False
    supports_reference_audio = False
    
    async def generate(
        self,
        prompt: str,
        **kwargs,
    ) -> GenerationResult:
        # Your implementation
        ...
```

See [Extending Guide](docs/guides/EXTENDING.md) for details.

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

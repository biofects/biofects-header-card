# **DO NOT USE**  Biofects Header Card

A customizable Home Assistant header card that displays a daily greeting and inspirational quote.

![Preview of Biofects Header Card](https://placeholder.image/screenshot.png)

## Features

- 🏠 Full-width header card for Home Assistant
- 💬 Dynamic daily quotes from multiple sources
- 🎨 Fully customizable
- 🔧 Easy configuration
- 📦 HACS Installation

## Prerequisites

- Home Assistant 2023.10 or newer
- HACS (Home Assistant Community Store)
- Python 3.9+

## Installation

### Step 1: Install via HACS

1. Open HACS in your Home Assistant
2. Click "Integrations"
3. Click the three-dot menu in the top right
4. Select "Custom Repositories"
5. Add repository URL: `https://github.com/biofects/biofects-header-card`
6. Choose category: "Integration"
7. Click "Add"
8. Search for "Biofects Header Card"
9. Click "Download"
10. Restart Home Assistant

### Step 2: Configuration

#### Option 1: Via `configuration.yaml`

```yaml
# configuration.yaml
sensor:
  - platform: biofects_header_card
    quote_feeds:
      # Optional: Add custom quote sources
      - url: 'https://www.brainyquote.com/link/quotefu.rss'
        type: rss
      - url: 'https://quotes.rest/qod.json'
        type: json
```

#### Option 2: Via Lovelace Card Configuration

```yaml
type: 'custom:biofects-header-card'
greeting: 'Hello, Welcome Home!'
quote_entity: sensor.biofects_daily_quote
```

## Configuration Options

### Quote Feeds

You can specify multiple quote sources with different types:

- `rss`: RSS Feed with quote in description
- `json`: JSON API with specific structure
- `type.fit`: Type.fit style API
- `auto`: Automatic detection of feed type

```yaml
quote_feeds:
  - url: 'https://www.brainyquote.com/link/quotefu.rss'
    type: rss
  - url: 'https://quotes.rest/qod.json'
    type: json
  - url: 'https://type.fit/api/quotes'
    type: auto
```

### Greeting Customization

Customize the greeting text:

```yaml
type: 'custom:biofects-header-card'
greeting: 'Welcome, {user}!'  # Optional dynamic greeting
```

### Card Styling with Card Mod

Use card-mod for advanced styling:

```yaml
type: 'custom:biofects-header-card'
card_mod:
  style:
    ha-card:
      background-color: rgba(0,0,0,0.1)
      border-radius: 10px
      font-family: 'Roboto, sans-serif'
```

## Troubleshooting

### No Quotes Appearing
- Ensure internet connection is stable
- Check Home Assistant logs for errors
- Verify quote feed URLs are accessible

### Custom Quote Sources
- Ensure URLs are publicly accessible
- Check URL format matches supported types (RSS/JSON)
- Use `type` parameter to specify feed type

## Acknowledgements

- Home Assistant Community
- Quote API Providers
- HACS Team

## Disclaimer

This project is a community contribution and is not officially supported by Home Assistant.

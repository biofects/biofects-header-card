"""Sensor platform for Biofects Header Card."""
import logging
import random
import requests
import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME, CONF_RESOURCES
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN, DEFAULT_QUOTE_FEEDS, FEED_TYPES

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "Biofects Daily Quote"

# Validation schema for quote sources
QUOTE_SOURCE_SCHEMA = vol.Schema({
    vol.Required('url'): cv.url,
    vol.Optional('type', default='auto'): vol.In(list(FEED_TYPES.keys()) + ['auto']),
})

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional('quote_feeds', default=[]): vol.Any(
        vol.Schema([QUOTE_SOURCE_SCHEMA]),
        cv.ensure_list
    )
})

def determine_feed_type(url):
    """Automatically determine feed type based on URL or content."""
    if '.rss' in url:
        return 'rss'
    elif 'type.fit' in url:
        return 'type.fit'
    elif url.endswith('.json'):
        return 'json'
    return None

def fetch_quote_from_rss(feed_url):
    """Fetch quote from RSS feed."""
    try:
        import feedparser
        feed = feedparser.parse(feed_url)
        if feed.entries:
            entry = random.choice(feed.entries)
            return {
                'quote': entry.get('description', 'No quote available'),
                'author': entry.get('title', 'Unknown')
            }
    except Exception as e:
        _LOGGER.error(f"Error fetching quote from RSS {feed_url}: {e}")
    return None

def fetch_quote_from_api(api_url, feed_type=None):
    """Fetch quote from API with optional type specification."""
    try:
        response = requests.get(api_url, timeout=10)
        data = response.json()
        
        # Determine feed type if not specified
        if feed_type == 'auto':
            feed_type = determine_feed_type(api_url)
        
        # Handle different API response structures
        if feed_type == 'json' and 'contents' in data and 'quotes' in data['contents']:
            # Quotes REST API
            quote = data['contents']['quotes'][0]
            return {
                'quote': quote.get('quote', 'No quote available'),
                'author': quote.get('author', 'Unknown')
            }
        elif feed_type in ['type.fit', 'auto']:
            # type.fit API or auto-detected
            if isinstance(data, list):
                quote = random.choice(data)
                return {
                    'quote': quote.get('text', 'No quote available'),
                    'author': quote.get('author', 'Unknown')
                }
    except Exception as e:
        _LOGGER.error(f"Error fetching quote from API {api_url}: {e}")
    return None

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Biofects Daily Quote sensor."""
    name = config.get(CONF_NAME)
    
    # Get user-defined quote feeds or use defaults
    quote_feeds = config.get('quote_feeds', [])
    if not quote_feeds:
        quote_feeds = [{'url': url, 'type': 'auto'} for url in DEFAULT_QUOTE_FEEDS]
    
    # Try to fetch quote from provided sources
    quote_data = None
    for feed in quote_feeds:
        url = feed['url']
        feed_type = feed['type']
        
        # Determine quote fetch method based on URL
        if url.endswith('.rss') or feed_type == 'rss':
            quote_data = fetch_quote_from_rss(url)
        else:
            quote_data = fetch_quote_from_api(url, feed_type)
        
        if quote_data:
            break

    # Fallback quote if all sources fail
    if not quote_data:
        quote_data = {
            'quote': 'Creativity is intelligence having fun.',
            'author': 'Albert Einstein'
        }

    quote_sensor = BiofectsQuoteSensor(name, quote_data)
    add_entities([quote_sensor])

class BiofectsQuoteSensor(Entity):
    """Representation of a Biofects Daily Quote Sensor."""

    def __init__(self, name, quote_data):
        """Initialize the sensor."""
        self._name = name
        self._quote = quote_data['quote']
        self._author = quote_data['author']
        self._state = self._quote

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return additional attributes."""
        return {
            'author': self._author
        }

    def update(self):
        """Update the sensor."""
        # You could implement periodic quote refresh here if needed
        pass

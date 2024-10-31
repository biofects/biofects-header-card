class BiofectsHeaderCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  setConfig(config) {
    const root = this.shadowRoot;
    if (root.lastChild) root.removeChild(root.lastChild);
    
    const card = document.createElement('ha-card');
    const content = document.createElement('div');
    content.style.padding = '16px';
    
    // Default values
    const greeting = config.greeting || 'Welcome Home';
    const quoteEntity = config.quote_entity || 'sensor.biofects_daily_quote';
    const quoteAuthorEntity = config.quote_author_entity || 'sensor.biofects_daily_quote';

    const greetingEl = document.createElement('h2');
    greetingEl.textContent = greeting;
    content.appendChild(greetingEl);

    const quoteEl = document.createElement('p');
    quoteEl.style.fontStyle = 'italic';
    content.appendChild(quoteEl);

    const authorEl = document.createElement('p');
    authorEl.style.textAlign = 'right';
    authorEl.style.fontWeight = 'bold';
    content.appendChild(authorEl);

    card.appendChild(content);
    root.appendChild(card);

    this._config = config;
  }

  set hass(hass) {
    const root = this.shadowRoot;
    const quoteEl = root.querySelector('p:nth-child(2)');
    const authorEl = root.querySelector('p:nth-child(3)');

    const quote = hass.states[this._config.quote_entity || 'sensor.biofects_daily_quote'];
    const author = hass.states[this._config.quote_author_entity || 'sensor.biofects_daily_quote'];

    if (quote) {
      quoteEl.textContent = `"${quote.state}"`;
    }

    if (author && author.attributes && author.attributes.author) {
      authorEl.textContent = `- ${author.attributes.author}`;
    }
  }

  getCardSize() {
    return 2;
  }
}

customElements.define('biofects-header-card', BiofectsHeaderCard);

window.customCards = window.customCards || [];
window.customCards.push({
  type: 'biofects-header-card',
  name: 'Biofects Header Card',
  preview: true,
  description: 'A header card with a daily greeting and quote'
});

(function () {
  'use strict';

  var CONFIG = {
    apiKey: '',
    avatars: {}
  };

  function avatarUrl(key) {
    return CONFIG.avatars[key] || '';
  }

  function avatarHtml(key, fallbackEmoji) {
    var url = avatarUrl(key);
    if (url) {
      return '<img src="' + url + '" alt="" style="width:100%;height:100%;object-fit:cover;border-radius:50%">';
    }
    return fallbackEmoji;
  }

  var DOCTORS = {
    female: {
      name: 'Dr. Elena',
      label: 'Caring & Warm',
      emoji: '\uD83D\uDC69\u200D\u2695\uFE0F',
      prompt: 'You are Dr. Elena, a warm and caring doctor. Speak with kindness, empathy, and a gentle bedside manner — like a trusted family physician who truly listens. If the user asks something off-topic (not health-related), gently steer them back with warmth. For example: "That\'s an interesting question! While I\'m here to help with health topics, is there something about your wellbeing I can assist with? \uD83D\uDE0A" Always include: "This is for informational purposes only, not medical advice. In emergencies, contact your doctor or emergency services." Never diagnose or prescribe.'
    },
    male: {
      name: 'Dr. James',
      label: 'Cold & Professional',
      emoji: '\uD83D\uDC68\u200D\u2695\uFE0F',
      prompt: 'You are Dr. James, a cold and strictly professional doctor. Be direct, concise, and clinical. No pleasantries, no warmth — just precise medical information. If the user asks something off-topic, state flatly: "That is outside my scope. Please ask a health-related question." Always include: "This is for informational purposes only, not medical advice. In emergencies, contact your doctor or emergency services." Never diagnose or prescribe.'
    }
  };

  var state = {
    isOpen: false,
    selectedDoctor: 'female',
    messages: [],
    isLoading: false,
    conversations: []
  };

  var els = {};

  function loadConversations() {
    try {
      var raw = localStorage.getItem('hb_convs');
      return raw ? JSON.parse(raw) : [];
    } catch (e) {
      return [];
    }
  }

  function saveConversations() {
    try {
      localStorage.setItem('hb_convs', JSON.stringify(state.conversations));
    } catch (e) {}
  }

  function injectStyles() {
    if (document.getElementById('hb-styles')) return;

    var css = [
      '#hbuddy *,#hbuddy *::before,#hbuddy *::after{box-sizing:border-box;margin:0;padding:0}',
      '#hbuddy{font-family:"Segoe UI",system-ui,-apple-system,sans-serif;position:fixed;z-index:2147483647;bottom:24px;right:24px}',
      '#hbuddy .hb-bubble{width:60px;height:60px;border-radius:50%;background:linear-gradient(135deg,#E63946,#8B0000);border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 20px rgba(230,57,70,0.4);transition:transform .2s,box-shadow .2s;position:relative;animation:hb-float 3s ease-in-out infinite}',
      '#hbuddy .hb-bubble:hover{transform:scale(1.08);box-shadow:0 6px 28px rgba(230,57,70,0.55);animation:none}',
      '#hbuddy .hb-bubble svg{width:28px;height:28px;fill:#fff;transition:transform .3s}',
      '#hbuddy .hb-bubble.hb-open svg{transform:rotate(45deg)}',
      '#hbuddy .hb-popup{position:absolute;bottom:76px;right:0;width:380px;height:600px;max-height:calc(100vh - 120px);background:#0a0a0a;border-radius:16px;border:1px solid rgba(230,57,70,0.15);box-shadow:0 20px 60px rgba(0,0,0,0.6),0 0 40px rgba(230,57,70,0.08);display:flex;flex-direction:column;overflow:hidden;opacity:0;transform:translateY(16px) scale(0.95);pointer-events:none;transition:opacity .3s,transform .3s cubic-bezier(0.16,1,0.3,1);transform-origin:bottom right}',
      '#hbuddy .hb-popup.hb-visible{opacity:1;transform:translateY(0) scale(1);pointer-events:all}',
      '#hbuddy .hb-header{display:flex;align-items:center;justify-content:space-between;padding:16px 18px;border-bottom:1px solid rgba(230,57,70,0.1);flex-shrink:0}',
      '#hbuddy .hb-header-left{display:flex;align-items:center;gap:10px}',
      '#hbuddy .hb-header-icon{width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,rgba(230,57,70,0.2),rgba(139,0,0,0.2));display:flex;align-items:center;justify-content:center;font-size:18px}',
      '#hbuddy .hb-header-info h3{font-size:14px;font-weight:600;color:#e8e0e0}',
      '#hbuddy .hb-header-info span{font-size:11px;color:rgba(230,57,70,0.7);text-transform:uppercase;letter-spacing:.05em}',
      '#hbuddy .hb-header-close{background:none;border:none;color:rgba(171,137,135,0.5);cursor:pointer;font-size:22px;padding:4px 8px;border-radius:6px;transition:all .2s;line-height:1}',
      '#hbuddy .hb-header-close:hover{background:rgba(230,57,70,0.1);color:#e8e0e0}',
      '#hbuddy .hb-header-right{display:flex;align-items:center;gap:4px}',
      '#hbuddy .hb-sidebar-btn{background:none;border:none;color:rgba(171,137,135,0.5);cursor:pointer;font-size:18px;padding:4px 8px;border-radius:6px;transition:all .2s;line-height:1}',
      '#hbuddy .hb-sidebar-btn:hover{background:rgba(230,57,70,0.1);color:#e8e0e0}',
      '#hbuddy .hb-doctors{display:flex;gap:6px;padding:10px 18px;border-bottom:1px solid rgba(230,57,70,0.06);flex-shrink:0}',
      '#hbuddy .hb-doc-btn{flex:1;padding:8px 10px;border-radius:10px;border:1px solid rgba(230,57,70,0.12);background:rgba(18,18,18,0.8);color:rgba(171,137,135,0.6);cursor:pointer;text-align:center;transition:all .2s;font-size:12px;font-family:inherit}',
      '#hbuddy .hb-doc-btn .hb-doc-emoji{font-size:20px;display:block;margin-bottom:2px}',
      '#hbuddy .hb-doc-btn .hb-doc-emoji img{width:36px;height:36px;border-radius:50%;object-fit:cover;display:block;margin:0 auto}',
      '#hbuddy .hb-doc-btn .hb-doc-name{font-weight:600;font-size:12px;display:block}',
      '#hbuddy .hb-doc-btn .hb-doc-label{font-size:9px;text-transform:uppercase;letter-spacing:.05em;opacity:.6}',
      '#hbuddy .hb-doc-btn.hb-active{border-color:#E63946;background:rgba(230,57,70,0.1);color:#e8e0e0;box-shadow:0 0 12px rgba(230,57,70,0.15)}',
      '#hbuddy .hb-sidebar-overlay{position:absolute;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.5);z-index:10;display:none}',
      '#hbuddy .hb-sidebar-overlay.hb-visible{display:block}',
      '#hbuddy .hb-sidebar{position:absolute;top:0;right:0;bottom:0;width:100%;max-width:380px;background:#0d0d0d;border-left:1px solid rgba(230,57,70,0.12);z-index:11;display:none;flex-direction:column;padding:24px 20px}',
      '#hbuddy .hb-sidebar.hb-visible{display:flex}',
      '#hbuddy .hb-sidebar-title{font-size:15px;font-weight:600;color:#e8e0e0;margin-bottom:16px;text-align:center;padding-bottom:14px;border-bottom:1px solid rgba(230,57,70,0.08)}',
      '#hbuddy .hb-sidebar .hb-doctors{display:flex;flex-direction:column;gap:8px;padding:0;border:none}',
      '#hbuddy .hb-sidebar .hb-doc-btn{flex:none;display:flex;align-items:center;gap:12px;padding:14px 12px;text-align:left;width:100%}',
      '#hbuddy .hb-sidebar .hb-doc-btn .hb-doc-emoji{display:inline-flex;margin:0;width:36px;height:36px;align-items:center;justify-content:center;flex-shrink:0}',
      '#hbuddy .hb-sidebar .hb-doc-btn .hb-doc-info{display:flex;flex-direction:column;gap:2px;min-width:0;flex:1}',
      '#hbuddy .hb-sidebar .hb-doc-btn .hb-doc-name{font-size:13px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}',
      '#hbuddy .hb-sidebar .hb-doc-btn .hb-doc-label{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}',
      '#hbuddy .hb-messages{flex:1;overflow-y:auto;padding:16px 18px;display:flex;flex-direction:column;gap:12px}',
      '#hbuddy .hb-messages::-webkit-scrollbar{width:4px}',
      '#hbuddy .hb-messages::-webkit-scrollbar-track{background:transparent}',
      '#hbuddy .hb-messages::-webkit-scrollbar-thumb{background:rgba(230,57,70,0.2);border-radius:2px}',
      '#hbuddy .hb-msg{display:flex;gap:10px;animation:hb-slideUp .3s cubic-bezier(0.16,1,0.3,1) forwards;max-width:90%}',
      '#hbuddy .hb-msg.hb-user{align-self:flex-end;flex-direction:row-reverse}',
      '#hbuddy .hb-msg-avatar{width:32px;height:32px;min-width:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:16px;box-shadow:0 0 0 2px rgba(230,57,70,0.12);flex-shrink:0;background:linear-gradient(135deg,rgba(58,74,107,0.3),rgba(30,40,60,0.3))}',
      '#hbuddy .hb-msg.hb-user .hb-msg-avatar{background:linear-gradient(135deg,rgba(230,57,70,0.2),rgba(139,0,0,0.2))}',
      '#hbuddy .hb-msg-bubble{padding:10px 14px;border-radius:12px;font-size:14px;line-height:1.6;word-wrap:break-word}',
      '#hbuddy .hb-msg.hb-user .hb-msg-bubble{background:linear-gradient(135deg,rgba(42,18,18,0.95),rgba(30,12,12,0.95));border:1px solid rgba(230,57,70,0.12);color:#e8e0e0;border-radius:4px 14px 14px 14px}',
      '#hbuddy .hb-msg.hb-assistant.hb-doc-female .hb-msg-bubble{background:linear-gradient(135deg,rgba(42,18,18,0.95),rgba(30,12,12,0.95));border-left:3px solid #E63946;color:#f5ecec;border-radius:4px 14px 14px 14px}',
      '#hbuddy .hb-msg.hb-assistant.hb-doc-male .hb-msg-bubble{background:linear-gradient(135deg,rgba(12,14,18,0.98),rgba(8,10,14,0.98));border-left:3px solid #3a4a6b;color:#c8ccd0;border-radius:2px 10px 10px 10px}',
      '#hbuddy .hb-typing{display:flex;gap:10px;padding:0 18px 8px;animation:hb-slideUp .2s ease forwards;align-items:flex-start}',
      '#hbuddy .hb-typing .hb-msg-avatar{width:32px;height:32px;min-width:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,rgba(58,74,107,0.3),rgba(30,40,60,0.3));font-size:16px;flex-shrink:0}',
      '#hbuddy .hb-typing .hb-msg-bubble{display:flex;gap:4px;padding:14px 18px;background:rgba(42,18,18,0.5);border-left:3px solid #E63946;border-radius:4px 14px 14px 14px}',
      '#hbuddy .hb-typing-dot{width:8px;height:8px;border-radius:50%;background:rgba(230,57,70,0.5);animation:hb-dotPulse 1.4s ease-in-out infinite}',
      '#hbuddy .hb-typing-dot:nth-child(2){animation-delay:.2s}',
      '#hbuddy .hb-typing-dot:nth-child(3){animation-delay:.4s}',
      '#hbuddy .hb-input-area{padding:12px 18px;border-top:1px solid rgba(230,57,70,0.08);flex-shrink:0}',
      '#hbuddy .hb-input-wrap{display:flex;gap:8px;background:rgba(18,18,18,0.8);border:1px solid rgba(230,57,70,0.15);border-radius:10px;padding:4px;transition:border-color .2s}',
      '#hbuddy .hb-input-wrap:focus-within{border-color:rgba(230,57,70,0.5)}',
      '#hbuddy .hb-input-wrap input{flex:1;background:none;border:none;outline:none;padding:8px 10px;font-size:14px;color:#e5e2e1;font-family:inherit}',
      '#hbuddy .hb-input-wrap input::placeholder{color:rgba(91,64,63,0.6)}',
      '#hbuddy .hb-input-wrap button{width:38px;height:38px;border-radius:8px;border:none;background:linear-gradient(135deg,#E63946,#8B0000);color:#fff;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all .2s;flex-shrink:0}',
      '#hbuddy .hb-input-wrap button:hover{background:linear-gradient(135deg,#ff525b,#a00000);transform:scale(1.05)}',
      '#hbuddy .hb-input-wrap button:disabled{opacity:.4;cursor:not-allowed;transform:none}',
      '#hbuddy .hb-input-wrap button svg{width:18px;height:18px;fill:#fff}',
      '#hbuddy .hb-empty{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:32px 24px;text-align:center}',
      '#hbuddy .hb-empty-icon{font-size:40px;margin-bottom:12px}',
      '#hbuddy .hb-empty h4{font-size:16px;color:#e8e0e0;margin-bottom:4px;font-weight:600}',
      '#hbuddy .hb-empty p{font-size:13px;color:rgba(171,137,135,0.5);max-width:240px;line-height:1.5}',
      '#hbuddy .hb-error{position:absolute;bottom:76px;left:18px;right:18px;background:rgba(230,57,70,0.95);color:#fff;padding:12px 16px;border-radius:10px;font-size:13px;text-align:center;animation:hb-slideUp .3s ease;z-index:10}',
      '#hbuddy .hb-history-btn{background:none;border:none;color:rgba(171,137,135,0.5);cursor:pointer;font-size:16px;padding:4px 6px;border-radius:6px;transition:all .2s;line-height:1}',
      '#hbuddy .hb-history-btn:hover{background:rgba(230,57,70,0.1);color:#e8e0e0}',
      '#hbuddy .hb-history-sidebar{position:absolute;top:0;left:0;right:0;bottom:0;width:100%;max-width:380px;background:#0d0d0d;border-right:1px solid rgba(230,57,70,0.12);z-index:12;display:none;flex-direction:column;padding:20px 16px}',
      '#hbuddy .hb-history-sidebar.hb-visible{display:flex}',
      '#hbuddy .hb-history-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;padding-bottom:12px;border-bottom:1px solid rgba(230,57,70,0.08)}',
      '#hbuddy .hb-history-header h3{font-size:15px;font-weight:600;color:#e8e0e0;margin:0}',
      '#hbuddy .hb-history-header button{background:none;border:none;color:rgba(171,137,135,0.4);cursor:pointer;font-size:18px;padding:2px 6px;border-radius:4px;line-height:1}',
      '#hbuddy .hb-history-header button:hover{background:rgba(230,57,70,0.1);color:#e8e0e0}',
      '#hbuddy .hb-new-chat-btn{width:100%;padding:10px;border-radius:8px;border:1px solid rgba(230,57,70,0.2);background:rgba(230,57,70,0.08);color:#e8e0e0;cursor:pointer;font-size:13px;font-weight:600;font-family:inherit;margin-bottom:14px;transition:all .2s}',
      '#hbuddy .hb-new-chat-btn:hover{background:rgba(230,57,70,0.15);border-color:#E63946}',
      '#hbuddy .hb-history-list{flex:1;overflow-y:auto;display:flex;flex-direction:column;gap:6px}',
      '#hbuddy .hb-history-list::-webkit-scrollbar{width:4px}',
      '#hbuddy .hb-history-list::-webkit-scrollbar-track{background:transparent}',
      '#hbuddy .hb-history-list::-webkit-scrollbar-thumb{background:rgba(230,57,70,0.2);border-radius:2px}',
      '#hbuddy .hb-history-item{display:flex;align-items:center;gap:6px;padding:10px 10px;border-radius:8px;cursor:pointer;transition:background .15s;border:none;background:none;color:#c8bfbe;font-size:13px;font-family:inherit;text-align:left;width:100%}',
      '#hbuddy .hb-history-item:hover{background:rgba(230,57,70,0.06)}',
      '#hbuddy .hb-history-item .hb-hi-title{flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}',
      '#hbuddy .hb-history-item .hb-hi-del{background:none;border:none;color:rgba(171,137,135,0.3);cursor:pointer;font-size:14px;padding:2px 4px;border-radius:4px;line-height:1;flex-shrink:0}',
      '#hbuddy .hb-history-item .hb-hi-del:hover{color:#E63946;background:rgba(230,57,70,0.1)}',
      '#hbuddy .hb-history-empty{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;color:rgba(171,137,135,0.4);font-size:13px;text-align:center;padding:32px 16px}',
      '#hbuddy .hb-history-empty span{font-size:32px;margin-bottom:8px}',
      '@keyframes hb-float{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}',
      '@keyframes hb-slideUp{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}',
      '@keyframes hb-dotPulse{0%,80%,100%{transform:scale(0.6);opacity:.3}40%{transform:scale(1);opacity:1}}',
      '@media(max-width:480px){',
      '#hbuddy{bottom:0;right:0;left:0}',
      '#hbuddy .hb-popup{position:fixed;bottom:0;right:0;left:0;top:0;width:100%;height:100%;max-height:100%;border-radius:0;border:none;transform:translateY(20px) scale(1)}',
      '#hbuddy .hb-popup.hb-visible{transform:translateY(0)}',
      '#hbuddy .hb-bubble{margin-right:16px;margin-bottom:16px}',
      '}'
    ].join('');

    var style = document.createElement('style');
    style.id = 'hb-styles';
    style.textContent = css;
    document.head.appendChild(style);
  }

  function buildWidget() {
    var container = document.getElementById('heal-buddy-widget');
    if (!container) {
      container = document.createElement('div');
      container.id = 'heal-buddy-widget';
      document.body.appendChild(container);
    }
    container.id = 'hbuddy';

    container.innerHTML = [
      '<button class="hb-bubble" id="hb-bubble" aria-label="Open chat">',
      '<svg viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H5.17L4 17.17V4h16v12z"/><path d="M7 9h10v2H7zm0-3h10v2H7zm0 6h7v2H7z"/></svg>',
      '</button>',
      '<div class="hb-popup" id="hb-popup">',
      '<div class="hb-header">',
      '<div class="hb-header-left">',
      '<div class="hb-header-icon">\uD83D\uDC89</div>',
      '<div class="hb-header-info"><h3>Heal Buddy</h3><span>Medical Information Assistant</span></div>',
      '</div>',
      '<div class="hb-header-right">',
      '<button class="hb-history-btn" id="hb-history-btn" aria-label="History">\uD83D\uDCCB</button>',
      '<button class="hb-sidebar-btn" id="hb-sidebar-btn" aria-label="Switch doctor">\uD83D\uDC64</button>',
      '<button class="hb-header-close" id="hb-close" aria-label="Close chat">\u2715</button>',
      '</div>',
      '</div>',
      '<div class="hb-messages" id="hb-messages">',
      '<div class="hb-empty" id="hb-empty">',
      '<div class="hb-empty-icon">\uD83D\uDC89</div>',
      '<h4>How can I help you?</h4>',
      '<p>Describe your symptoms or ask a health-related question.</p>',
      '</div>',
      '</div>',
      '<div class="hb-input-area">',
      '<div class="hb-input-wrap">',
      '<input type="text" id="hb-input" placeholder="Describe your symptoms..." autocomplete="off">',
      '<button id="hb-send" aria-label="Send message">',
      '<svg viewBox="0 0 24 24"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>',
      '</button>',
      '</div>',
      '</div>',
      '<div class="hb-sidebar-overlay" id="hb-sidebar-overlay"></div>',
      '<div class="hb-sidebar" id="hb-sidebar">',
      '<div class="hb-sidebar-title">Choose Your Doctor</div>',
      '<div class="hb-doctors" id="hb-doctors"></div>',
      '</div>',
      '<div class="hb-history-sidebar" id="hb-history-sidebar">',
      '<div class="hb-history-header">',
      '<h3>\uD83D\uDCCB History</h3>',
      '<button id="hb-history-close">\u2715</button>',
      '</div>',
      '<button class="hb-new-chat-btn" id="hb-new-chat-btn">➕ New Chat</button>',
      '<div class="hb-history-list" id="hb-history-list"></div>',
      '</div>',
      '</div>'
    ].join('');

    els.bubble = document.getElementById('hb-bubble');
    els.popup = document.getElementById('hb-popup');
    els.close = document.getElementById('hb-close');
    els.messages = document.getElementById('hb-messages');
    els.input = document.getElementById('hb-input');
    els.send = document.getElementById('hb-send');
    els.doctors = document.getElementById('hb-doctors');
    els.empty = document.getElementById('hb-empty');
    els.sidebar = document.getElementById('hb-sidebar');
    els.sidebarOverlay = document.getElementById('hb-sidebar-overlay');
    els.sidebarBtn = document.getElementById('hb-sidebar-btn');
    els.historySidebar = document.getElementById('hb-history-sidebar');
    els.historyBtn = document.getElementById('hb-history-btn');
    els.historyClose = document.getElementById('hb-history-close');
    els.historyList = document.getElementById('hb-history-list');
    els.newChatBtn = document.getElementById('hb-new-chat-btn');
  }

  function renderDoctors() {
    els.doctors.innerHTML = '';
    Object.keys(DOCTORS).forEach(function (key) {
      var doc = DOCTORS[key];
      var btn = document.createElement('button');
      btn.className = 'hb-doc-btn' + (key === state.selectedDoctor ? ' hb-active' : '');
      var avatar = avatarHtml(key, doc.emoji);
      btn.innerHTML = '<span class="hb-doc-emoji">' + avatar + '</span><div class="hb-doc-info"><span class="hb-doc-name">' + doc.name + '</span><span class="hb-doc-label">' + doc.label + '</span></div>';
      btn.addEventListener('click', function () {
        state.selectedDoctor = key;
        renderDoctors();
        closeSidebar();
      });
      els.doctors.appendChild(btn);
    });
  }

  function openSidebar() {
    els.sidebar.classList.add('hb-visible');
    els.sidebarOverlay.classList.add('hb-visible');
  }

  function closeSidebar() {
    els.sidebar.classList.remove('hb-visible');
    els.sidebarOverlay.classList.remove('hb-visible');
  }

  function toggleSidebar() {
    if (els.sidebar.classList.contains('hb-visible')) {
      closeSidebar();
    } else {
      closeHistorySidebar();
      openSidebar();
    }
  }

  function openHistorySidebar() {
    renderHistory();
    els.historySidebar.classList.add('hb-visible');
  }

  function closeHistorySidebar() {
    els.historySidebar.classList.remove('hb-visible');
  }

  function toggleHistorySidebar() {
    if (els.historySidebar.classList.contains('hb-visible')) {
      closeHistorySidebar();
    } else {
      closeSidebar();
      openHistorySidebar();
    }
  }

  function getConversationTitle() {
    for (var i = 0; i < state.messages.length; i++) {
      if (state.messages[i].role === 'user') {
        var content = state.messages[i].content;
        return content.length > 50 ? content.substring(0, 50) + '...' : content;
      }
    }
    return 'Chat';
  }

  function newChat() {
    if (state.messages.length > 0) {
      state.conversations.push({
        id: Date.now(),
        title: getConversationTitle(),
        messages: JSON.parse(JSON.stringify(state.messages)),
        doctor: state.selectedDoctor
      });
      saveConversations();
    }
    state.messages = [];
    renderMessages();
    closeHistorySidebar();
    renderHistory();
  }

  function loadConversation(id) {
    for (var i = 0; i < state.conversations.length; i++) {
      if (state.conversations[i].id === id) {
        if (state.messages.length > 0) {
          state.conversations.push({
            id: Date.now(),
            title: getConversationTitle(),
            messages: JSON.parse(JSON.stringify(state.messages)),
            doctor: state.selectedDoctor
          });
        }
        state.messages = JSON.parse(JSON.stringify(state.conversations[i].messages));
        state.selectedDoctor = state.conversations[i].doctor || 'female';
        saveConversations();
        renderMessages();
        renderDoctors();
        closeHistorySidebar();
        return;
      }
    }
  }

  function deleteConversation(id) {
    state.conversations = state.conversations.filter(function (c) { return c.id !== id; });
    saveConversations();
    renderHistory();
  }

  function renderHistory() {
    els.historyList.innerHTML = '';
    if (state.conversations.length === 0) {
      els.historyList.innerHTML = '<div class="hb-history-empty"><span>\uD83D\uDCCB</span>No saved chats yet</div>';
      return;
    }
    for (var i = state.conversations.length - 1; i >= 0; i--) {
      var conv = state.conversations[i];
      var item = document.createElement('button');
      item.className = 'hb-history-item';
      item.setAttribute('data-id', conv.id);
      item.innerHTML = '<span class="hb-hi-title">\uD83D\uDCAC ' + conv.title + '</span><span class="hb-hi-del">\u2715</span>';
      item.addEventListener('click', function (e) {
        if (e.target.classList.contains('hb-hi-del')) {
          var id = parseInt(e.target.closest('.hb-history-item').getAttribute('data-id'));
          deleteConversation(id);
          return;
        }
        var id = parseInt(this.getAttribute('data-id'));
        loadConversation(id);
      });
      els.historyList.appendChild(item);
    }
  }

  function renderMessages() {
    if (state.messages.length === 0) {
      els.empty.style.display = 'flex';
      els.messages.querySelectorAll('.hb-msg').forEach(function (el) { el.remove(); });
      return;
    }
    els.empty.style.display = 'none';

    var existing = els.messages.querySelectorAll('.hb-msg');
    if (existing.length === state.messages.length) return;

    els.messages.querySelectorAll('.hb-msg').forEach(function (el) { el.remove(); });

    state.messages.forEach(function (msg) {
      var isUser = msg.role === 'user';
      var docKey = msg.doctor || 'female';
      var div = document.createElement('div');
      div.className = 'hb-msg hb-' + (isUser ? 'user' : 'assistant') + ' hb-doc-' + docKey;
      var avHtml = isUser ? avatarHtml('user', '\uD83D\uDC64') : avatarHtml(docKey, DOCTORS[docKey].emoji);
      div.innerHTML = '<div class="hb-msg-avatar">' + avHtml + '</div><div class="hb-msg-bubble">' + escapeHtml(msg.content) + '</div>';
      els.messages.appendChild(div);
    });

    scrollToBottom();
  }

  function escapeHtml(text) {
    var div = document.createElement('div');
    div.appendChild(document.createTextNode(text));
    return div.innerHTML;
  }

  function scrollToBottom() {
    requestAnimationFrame(function () {
      els.messages.scrollTop = els.messages.scrollHeight;
    });
  }

  function showTyping() {
    if (els.messages.querySelector('.hb-typing')) return;
    var typing = document.createElement('div');
    var docKey = state.selectedDoctor;
    var doc = DOCTORS[docKey];
    var avHtml = avatarHtml(docKey, doc.emoji);
    typing.className = 'hb-typing';
    typing.innerHTML = '<div class="hb-msg-avatar">' + avHtml + '</div><div class="hb-msg-bubble"><div class="hb-typing-dot"></div><div class="hb-typing-dot"></div><div class="hb-typing-dot"></div></div>';
    els.messages.appendChild(typing);
    scrollToBottom();
  }

  function hideTyping() {
    var typing = els.messages.querySelector('.hb-typing');
    if (typing) typing.remove();
  }

  function showError(msg) {
    var existing = els.popup.querySelector('.hb-error');
    if (existing) existing.remove();
    var errEl = document.createElement('div');
    errEl.className = 'hb-error';
    errEl.textContent = msg;
    els.popup.appendChild(errEl);
    setTimeout(function () { errEl.remove(); }, 5000);
  }

  async function sendToAPI(userMsg) {
    if (!CONFIG.apiKey) {
      throw new Error('Groq API key not configured. Call HealBuddyWidget.init({ apiKey: "gsk_..." })');
    }

    var systemMsg = DOCTORS[state.selectedDoctor].prompt;

    var payload = {
      model: 'llama-3.3-70b-versatile',
      messages: [
        { role: 'system', content: systemMsg },
        { role: 'user', content: userMsg }
      ]
    };

    var res = await fetch('https://api.groq.com/openai/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + CONFIG.apiKey,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      var errText = await res.text();
      throw new Error('API error (' + res.status + '): ' + errText);
    }

    var data = await res.json();
    return data.choices[0].message.content;
  }

  async function handleSend() {
    var text = els.input.value.trim();
    if (!text || state.isLoading) return;

    els.input.value = '';
    state.isLoading = true;
    els.send.disabled = true;

    state.messages.push({ role: 'user', content: text });
    renderMessages();

    showTyping();

    try {
      var reply = await sendToAPI(text);
      hideTyping();
      state.messages.push({ role: 'assistant', content: reply, doctor: state.selectedDoctor });
      renderMessages();
    } catch (err) {
      hideTyping();
      showError(err.message);
    }

    state.isLoading = false;
    els.send.disabled = false;
    els.input.focus();
  }

  function open() {
    state.isOpen = true;
    els.bubble.classList.add('hb-open');
    els.popup.classList.add('hb-visible');
    renderMessages();
    setTimeout(function () { els.input.focus(); }, 350);
  }

  function close() {
    state.isOpen = false;
    els.bubble.classList.remove('hb-open');
    els.popup.classList.remove('hb-visible');
  }

  function toggle() {
    state.isOpen ? close() : open();
  }

  function init(config) {
    if (config) {
      if (config.apiKey) CONFIG.apiKey = config.apiKey;
      if (config.avatars) {
        if (config.avatars.user) CONFIG.avatars.user = config.avatars.user;
        if (config.avatars.female) CONFIG.avatars.female = config.avatars.female;
        if (config.avatars.male) CONFIG.avatars.male = config.avatars.male;
      }
    }

    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', setup);
    } else {
      setup();
    }
  }

  function setup() {
    injectStyles();
    buildWidget();

    localStorage.removeItem('hb_msgs');
    state.messages = [];
    state.conversations = loadConversations();

    renderDoctors();
    renderMessages();

    els.bubble.addEventListener('click', toggle);
    els.close.addEventListener('click', close);
    els.sidebarBtn.addEventListener('click', toggleSidebar);
    els.sidebarOverlay.addEventListener('click', closeSidebar);
    els.historyBtn.addEventListener('click', toggleHistorySidebar);
    els.historyClose.addEventListener('click', closeHistorySidebar);
    els.newChatBtn.addEventListener('click', newChat);
    els.send.addEventListener('click', handleSend);
    els.input.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') handleSend();
    });

    scrollToBottom();
  }

  window.HealBuddyWidget = {
    init: init,
    open: open,
    close: close,
    toggle: toggle,
    newChat: newChat
  };
})();

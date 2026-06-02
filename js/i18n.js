(function (window, document) {
	'use strict';

	var STORAGE_KEY = 'ladybug-lang';

	function getLang() {
		return localStorage.getItem(STORAGE_KEY) === 'zh' ? 'zh' : 'en';
	}

	function updatePageTitle(lang) {
		var titleEl = document.querySelector('title[data-title-en]');
		if (titleEl) {
			document.title = lang === 'zh'
				? titleEl.getAttribute('data-title-zh')
				: titleEl.getAttribute('data-title-en');
		}
	}

	function setLang(lang) {
		lang = lang === 'zh' ? 'zh' : 'en';
		localStorage.setItem(STORAGE_KEY, lang);
		document.documentElement.lang = lang === 'zh' ? 'zh-CN' : 'en';
		updateSwitcher(lang);
		updatePageTitle(lang);
	}

	function updateSwitcher(lang) {
		document.querySelectorAll('.lang-switch .lang-btn').forEach(function (btn) {
			var active = btn.getAttribute('data-set-lang') === lang;
			btn.classList.toggle('is-active', active);
			btn.setAttribute('aria-pressed', active ? 'true' : 'false');
		});
	}

	function injectSwitcher() {
		var nav = document.querySelector('.main-navigation');
		if (!nav || document.querySelector('.lang-switch')) {
			return;
		}
		var wrap = document.createElement('div');
		wrap.className = 'lang-switch';
		wrap.setAttribute('role', 'group');
		wrap.setAttribute('aria-label', 'Language');
		wrap.innerHTML =
			'<button type="button" class="lang-btn" data-set-lang="en" aria-pressed="false">EN</button>' +
			'<button type="button" class="lang-btn" data-set-lang="zh" aria-pressed="false">中文</button>';
		nav.parentNode.insertBefore(wrap, nav);
		wrap.addEventListener('click', function (e) {
			var btn = e.target.closest('[data-set-lang]');
			if (btn) {
				setLang(btn.getAttribute('data-set-lang'));
			}
		});
	}

	window.LadybugI18n = { setLang: setLang, getLang: getLang };

	function patchFormPlaceholders() {
		var zh = document.documentElement.lang === 'zh-CN';
		document.querySelectorAll('[data-ph-en]').forEach(function (el) {
			el.placeholder = zh ? el.getAttribute('data-ph-zh') : el.getAttribute('data-ph-en');
		});
		document.querySelectorAll('[data-val-en]').forEach(function (el) {
			el.value = zh ? el.getAttribute('data-val-zh') : el.getAttribute('data-val-en');
		});
		document.querySelectorAll('[data-alt-en]').forEach(function (el) {
			el.alt = zh ? el.getAttribute('data-alt-zh') : el.getAttribute('data-alt-en');
		});
	}

	document.addEventListener('DOMContentLoaded', function () {
		injectSwitcher();
		setLang(getLang());
		patchFormPlaceholders();
		var obs = new MutationObserver(patchFormPlaceholders);
		obs.observe(document.documentElement, { attributes: true, attributeFilter: ['lang'] });
	});
})(window, document);

def init_plugin(browser):
    dark_css = """
        html, body {
            background: #111 !important;
            color: #eee !important;
        }
        * {
            background-color: transparent !important;
            color: #eee !important;
        }
        img, video {
            filter: brightness(0.8) contrast(1.2);
        }
    """

    js = f"""
        let style = document.createElement('style');
        style.innerHTML = `{dark_css}`;
        document.head.appendChild(style);
    """

    def apply_dark_mode():
        tab = browser.current_browser()
        if tab:
            tab.page().runJavaScript(js)

    # Apply on every page load
    browser.tabs.currentChanged.connect(lambda _: apply_dark_mode())
    browser.tabs.currentWidget().browser.loadFinished.connect(lambda _: apply_dark_mode())

    # Add toolbar toggle
    action = browser.toolbar.addAction("Force Dark Mode")
    action.triggered.connect(apply_dark_mode)
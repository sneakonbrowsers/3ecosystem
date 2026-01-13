from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import QUrl

def init_plugin(browser):
    urlbar = QLineEdit()
    urlbar.setPlaceholderText("Enter URL…")
    browser.toolbar.addWidget(urlbar)

    # Update bar when page loads
    def update_url():
        tab = browser.current_browser()
        if tab:
            urlbar.setText(tab.url().toString())

    browser.tabs.currentChanged.connect(lambda _: update_url())
    browser.tabs.currentWidget().browser.urlChanged.connect(lambda _: update_url())

    # Navigate when pressing Enter
    def navigate():
        text = urlbar.text().strip()
        if not text:
            return
        if "://" not in text:
            text = "https://" + text
        browser.current_browser().setUrl(QUrl(text))

    urlbar.returnPressed.connect(navigate)
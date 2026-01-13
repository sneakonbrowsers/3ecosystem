from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem

def init_plugin(browser):
    tabs = browser.tabs

    # Hide the normal tab bar
    tabs.tabBar().hide()

    # Grab the central layout (TitleBar, then content)
    central_layout = browser.centralWidget().layout()

    # Remove the tabs widget from the vertical layout
    central_layout.removeWidget(tabs)

    # Create a new horizontal layout to hold sidebar + tabs
    hbox = QHBoxLayout()
    hbox.setContentsMargins(0, 0, 0, 0)
    hbox.setSpacing(0)

    # Create sidebar
    sidebar = QListWidget()
    sidebar.setFixedWidth(180)
    sidebar.setStyleSheet("""
        QListWidget {
            background-color: #1a1a1a;
            color: #f0f0f0;
            border-right: 1px solid #333;
        }
        QListWidget::item:selected {
            background-color: #00bbff;
            color: #000;
        }
    """)

    # Add sidebar (left) and tabs (right)
    hbox.addWidget(sidebar)
    hbox.addWidget(tabs)

    # Insert the new horizontal layout back into the central layout
    # Right below the TitleBar (index 1)
    central_layout.insertLayout(1, hbox)

    # Populate sidebar with tab names
    def refresh_sidebar():
        sidebar.clear()
        for i in range(tabs.count()):
            title = tabs.tabText(i)
            item = QListWidgetItem(title)
            sidebar.addItem(item)

        # Highlight current tab
        sidebar.setCurrentRow(tabs.currentIndex())

    refresh_sidebar()

    # Sync sidebar when tabs change
    tabs.currentChanged.connect(lambda _: refresh_sidebar())
    tabs.tabCloseRequested.connect(lambda _: refresh_sidebar())

    # Clicking sidebar switches tabs
    def on_sidebar_click():
        index = sidebar.currentRow()
        if index >= 0:
            tabs.setCurrentIndex(index)

    sidebar.currentRowChanged.connect(lambda _: on_sidebar_click())
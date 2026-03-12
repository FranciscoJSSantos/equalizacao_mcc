import sys
import os
import threading
import webbrowser
import time


def get_app_path():
    if getattr(sys, "frozen", False):
        return os.path.join(sys._MEIPASS, "app.py")
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.py")


def open_browser():
    time.sleep(3)
    webbrowser.open("http://localhost:8501")


if __name__ == "__main__":
    from streamlit.web.bootstrap import load_config_options
    load_config_options({
        "global.developmentMode": False,
        "server.headless": True,
        "browser.gatherUsageStats": False,
    })

    threading.Thread(target=open_browser, daemon=True).start()

    from streamlit.web import bootstrap
    bootstrap.run(
        get_app_path(),
        False,
        [],
        {},
    )

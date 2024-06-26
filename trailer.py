import webview
import keyboard
import threading
import clipboard
import sys


# URL of the IMDb trailer
url = sys.argv[1]
if url == 'c':
	url = clipboard.paste()
	
# JavaScript code to inject custom CSS
js_code = """
const style = document.createElement('style');
style.innerHTML = `
    :root {
        --ipt-font-family: Roboto,Helvetica,Arial,sans-serif;
        --ipt-font-root-size: 50%;
    }
`;
document.head.appendChild(style);
"""

def inject_js(window):
    window.evaluate_js(js_code)

def setup_keyboard_shortcuts(window):
    # Listen for 'q' and 'esc' keys to exit the application
    keyboard.add_hotkey('q', lambda: exit_app(window))
    keyboard.add_hotkey('esc', lambda: exit_app(window))

def exit_app(window):
    print("Exiting application...")
    window.destroy()

if __name__ == '__main__':
    # Create and configure the browser window
    window = webview.create_window('IMDb Trailer Browser', url, width=720, height=480, resizable=False)
    window.events.loaded += lambda: inject_js(window)  # Inject CSS when the page is loaded

    # Start keyboard shortcuts in a background thread
    keyboard_thread = threading.Thread(target=setup_keyboard_shortcuts, args=(window,))
    keyboard_thread.start()

    # Start the webview application in the main thread
    webview.start()

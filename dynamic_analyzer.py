import frida
import sys

# The JavaScript payload injected into the app's memory
HOOK_SCRIPT = """
Java.perform(function () {
    var Activity = Java.use('android.app.Activity');
    
    // Intercept the onResume method (called every time a screen appears)
    Activity.onResume.implementation = function () {
        // Send a message back to our Python script
        send("[+] Screen Opened: " + this.getClass().getName());
        
        // Let the original method run so the app doesn't crash
        this.onResume(); 
    };
});
"""

def on_message(message, data):
    """Handles messages sent back from the injected JavaScript."""
    if message['type'] == 'send':
        print(message['payload'])
    elif message['type'] == 'error':
        print(f"[-] Error: {message['stack']}")

def main():
    package_name = "io.appium.android.apis"
    print(f"[*] Injecting hooks into {package_name}...")
    
    try:
        # Connect to the emulator
        device = frida.get_usb_device()
        
        # Force-start the app in a suspended state
        pid = device.spawn([package_name])
        session = device.attach(pid)
        
        # Inject our JavaScript payload
        script = session.create_script(HOOK_SCRIPT)
        script.on('message', on_message)
        script.load()
        
        # Resume the app so it actually opens on screen
        device.resume(pid)
        print("[*] Hook injected! Click around the app in the emulator...")
        
        # Keep the Python script alive to listen for messages
        sys.stdin.read()
    except Exception as e:
        print(f"[-] Dynamic analysis failed: {e}")

if __name__ == "__main__":
    main()
import sys
import os

def main():
    # Check command line arguments for interface choice
    if len(sys.argv) > 1 and sys.argv[1] == "--gui":
        try:
            # Try to run tkinter GUI
            from tkinter_app import main as tkinter_main
            tkinter_main()
            return
        except ImportError as e:
            print(f"GUI not available: {e}")
            print("Falling back to console interface...")
    
    # Console interface as fallback
    from music_library.music_service import MusicService
    from music_library.logging import LoggerFactory
    from ui.console_ui import ConsoleUI
    
    print("=== Music Library Application ===")
    
    # Select logger type
    logger_type = input("Select logger type (1 - console, 2 - file): ")
    
    if logger_type == "2":
        logger = LoggerFactory.create_file_logger("music_app.log")
        print("File logging enabled (music_app.log)")
    else:
        logger = LoggerFactory.create_console_logger()
        print("Console logging enabled")
    
    # Create service with selected logger
    music_service = MusicService(logger)
    
    # Run user interface
    ui = ConsoleUI(music_service)
    ui.run()

if __name__ == "__main__":
    main()